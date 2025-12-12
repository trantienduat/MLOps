"""FastAPI application for MNIST digit classification."""

import base64
import io
import time
from pathlib import Path
from typing import Any, Optional

import mlflow
import numpy as np
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from PIL import Image
from prometheus_client import make_asgi_app

from src.api.schemas import ErrorResponse, HealthResponse, PredictionRequest, PredictionResponse
from src.monitoring.metrics import (
    active_requests,
    api_requests,
    model_confidence,
    prediction_counter,
    prediction_errors,
    prediction_latency,
)
from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MNIST Digit Classification API",
    description="Production-ready ML API for MNIST digit recognition",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Global model variable
model: Optional[Any] = None
model_version: str = "unknown"


def load_model_from_local_path() -> None:
    """Load model from a local path baked into the image."""

    global model, model_version

    if not config.MODEL_LOCAL_PATH:
        return

    resolved = Path(config.MODEL_LOCAL_PATH)
    if not resolved.exists():
        raise RuntimeError(
            f"MODEL_LOCAL_PATH set to '{config.MODEL_LOCAL_PATH}' but path does not exist"
        )

    logger.info("Loading model from local path: %s", resolved)
    model = mlflow.tensorflow.load_model(resolved.as_posix())
    model_version = f"local:{resolved.name}"
    logger.info("Model loaded successfully from local path")


def load_model_from_registry() -> None:
    """
    Load model from local path (if provided) or MLflow Model Registry.

    Raises:
        RuntimeError: If model loading fails.
    """
    global model, model_version

    # Prefer baked-in local model when provided
    if config.MODEL_LOCAL_PATH:
        try:
            load_model_from_local_path()
            return
        except Exception as local_error:
            logger.error("Failed to load local model: %s", local_error)
            if not config.ALLOW_RUN_FALLBACK:
                raise RuntimeError(f"Model loading failed: {local_error}") from local_error
            logger.info("Proceeding to registry/fallback load after local model failure")

    try:
        logger.info(f"Loading model '{config.MODEL_NAME}' from MLflow Registry...")
        mlflow.set_tracking_uri(config.get_mlflow_uri())

        # Load model from registry
        model_uri = f"models:/{config.MODEL_NAME}/{config.MODEL_STAGE}"
        model = mlflow.tensorflow.load_model(model_uri)

        # Get model version info
        from mlflow.tracking import MlflowClient

        client = MlflowClient()
        model_versions = client.get_latest_versions(config.MODEL_NAME, stages=[config.MODEL_STAGE])

        if model_versions:
            model_version = model_versions[0].version
            logger.info(f"Model loaded successfully: {config.MODEL_NAME} v{model_version}")
        else:
            logger.warning("Could not retrieve model version")

    except Exception as e:
        logger.error(f"Failed to load model from registry: {e}")

        if not config.ALLOW_RUN_FALLBACK:
            raise RuntimeError(f"Model loading failed: {e}") from e

        # Fallback: load best run from experiment (order by test_accuracy)
        try:
            from mlflow.tracking import MlflowClient

            logger.info(
                "Falling back to best run in experiment '%s' by metrics.test_accuracy",
                config.EXPERIMENT_NAME,
            )

            client = MlflowClient()
            experiment = client.get_experiment_by_name(config.EXPERIMENT_NAME)
            if not experiment:
                raise RuntimeError(
                    f"Experiment '{config.EXPERIMENT_NAME}' not found; cannot fallback to best run"
                )

            runs = client.search_runs(
                experiment_ids=[experiment.experiment_id],
                order_by=["metrics.test_accuracy DESC"],
                max_results=1,
            )

            if not runs:
                raise RuntimeError(
                    f"No runs found in experiment '{config.EXPERIMENT_NAME}' to fallback"
                )

            best_run = runs[0]
            fallback_uri = f"runs:/{best_run.info.run_id}/model"
            logger.info(
                "Loading fallback model from run %s (test_accuracy=%s)",
                best_run.info.run_id,
                best_run.data.metrics.get("test_accuracy"),
            )
            model = mlflow.tensorflow.load_model(fallback_uri)
            model_version = f"run:{best_run.info.run_id}"
            logger.info("Fallback model loaded successfully from best run")

        except Exception as fallback_error:
            logger.error(f"Fallback load failed: {fallback_error}")
            raise RuntimeError(f"Model loading failed: {fallback_error}") from fallback_error


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize application on startup."""
    logger.info("Starting MNIST Classification API...")
    config.validate()
    load_model_from_registry()
    logger.info("API ready to serve requests")


@app.middleware("http")
async def track_requests(request: Request, call_next: Any) -> Any:
    """Middleware to track API requests and latency."""
    active_requests.inc()
    start_time = time.time()

    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        logger.error(f"Request failed: {e}")
        status_code = 500
        raise
    finally:
        active_requests.dec()
        latency = time.time() - start_time

        # Track metrics
        api_requests.labels(
            method=request.method, endpoint=request.url.path, status_code=status_code
        ).inc()

        logger.info(
            f"{request.method} {request.url.path} - Status: {status_code} - Latency: {latency:.3f}s"
        )

    return response


@app.get("/", response_class=HTMLResponse)
async def root() -> str:
    """Serve the main HTML page."""
    try:
        with open("templates/index.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("index.html not found")
        raise HTTPException(status_code=404, detail="Frontend not found")


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        Health status including model information.
    """
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        model_name=config.MODEL_NAME,
        model_version=model_version,
    )


@app.post("/predict", response_model=PredictionResponse, responses={500: {"model": ErrorResponse}})
async def predict(request: PredictionRequest) -> PredictionResponse:
    """
    Predict digit from base64 encoded image.

    Args:
        request: Prediction request with base64 image.

    Returns:
        Prediction results with confidence scores.

    Raises:
        HTTPException: If prediction fails.
    """
    if model is None:
        prediction_errors.labels(error_type="model_not_loaded").inc()
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        with prediction_latency.time():
            # Decode base64 image
            image_data = request.image.split(",")[1] if "," in request.image else request.image
            image_bytes = base64.b64decode(image_data)

            # Process image
            image = Image.open(io.BytesIO(image_bytes)).convert("L")
            image = image.resize((28, 28))
            image_array = np.array(image).astype("float32") / 255.0
            image_array = np.expand_dims(image_array, axis=-1)
            image_array = np.expand_dims(image_array, axis=0)

            # Make prediction
            predictions = model.predict(image_array, verbose=0)[0]
            prediction = int(np.argmax(predictions))
            confidence = float(predictions[prediction])

            # Track metrics
            prediction_counter.labels(
                model_version=model_version, predicted_class=str(prediction)
            ).inc()
            model_confidence.set(confidence)

            logger.info(f"Prediction: {prediction}, Confidence: {confidence:.4f}")

            return PredictionResponse(
                prediction=prediction,
                confidence=confidence,
                probabilities=predictions.tolist(),
            )

    except Exception as e:
        prediction_errors.labels(error_type=type(e).__name__).inc()
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/api/info")
async def api_info() -> dict:
    """Get API information and configuration."""
    return {
        "name": "MNIST Classification API",
        "version": "1.0.0",
        "environment": config.ENVIRONMENT,
        "model_name": config.MODEL_NAME,
        "model_stage": config.MODEL_STAGE,
        "mlflow_uri": config.MLFLOW_TRACKING_URI,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower(),
    )
