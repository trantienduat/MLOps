"""Training pipeline for MNIST classification models."""
from typing import Any, Dict, Tuple

import matplotlib.pyplot as plt
import mlflow
import mlflow.tensorflow
import numpy as np
import numpy.typing as npt
from tensorflow import keras

from src.data.loader import load_mnist_data
from src.models.cnn import (
    create_baseline_model,
    create_improved_architecture_model,
    create_optimized_model,
    get_model_config,
)
from src.utils.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def train_model(
    model: keras.Model,
    x_train: npt.NDArray[np.float32],
    y_train: npt.NDArray[np.int64],
    x_test: npt.NDArray[np.float32],
    y_test: npt.NDArray[np.int64],
    learning_rate: float = 0.001,
    batch_size: int = 128,
    epochs: int = 5,
    run_name: str = "",
) -> Tuple[keras.Model, keras.callbacks.History]:
    """
    Train model with MLflow tracking.

    Args:
        model: Keras model to train.
        x_train: Training images.
        y_train: Training labels.
        x_test: Test images.
        y_test: Test labels.
        learning_rate: Learning rate for optimizer.
        batch_size: Batch size for training.
        epochs: Number of training epochs.
        run_name: Name for this MLflow run.

    Returns:
        Tuple of (trained model, training history).

    Raises:
        RuntimeError: If training fails.
    """
    try:
        with mlflow.start_run(run_name=run_name):
            logger.info(f"Starting training run: {run_name}")

            # Log parameters
            mlflow.log_param("learning_rate", learning_rate)
            mlflow.log_param("batch_size", batch_size)
            mlflow.log_param("epochs", epochs)
            mlflow.log_param("optimizer", "adam")
            mlflow.log_param("model_name", model.name)

            # Compile model
            model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
                loss="sparse_categorical_crossentropy",
                metrics=["accuracy"],
            )

            # Log model summary
            model_summary = []
            model.summary(print_fn=lambda x: model_summary.append(x))
            mlflow.log_text("\n".join(model_summary), "model_summary.txt")

            # Train model
            logger.info("Training model...")
            history = model.fit(
                x_train,
                y_train,
                batch_size=batch_size,
                epochs=epochs,
                validation_split=0.1,
                verbose=1,
            )

            # Evaluate on test set
            logger.info("Evaluating model on test set...")
            test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)

            # Log metrics
            mlflow.log_metric("test_loss", test_loss)
            mlflow.log_metric("test_accuracy", test_accuracy)

            # Log training history
            for epoch in range(epochs):
                mlflow.log_metric("train_loss", history.history["loss"][epoch], step=epoch)
                mlflow.log_metric("train_accuracy", history.history["accuracy"][epoch], step=epoch)
                mlflow.log_metric("val_loss", history.history["val_loss"][epoch], step=epoch)
                mlflow.log_metric("val_accuracy", history.history["val_accuracy"][epoch], step=epoch)

            # Create and log training curves
            _log_training_curves(history)

            # Log model with signature
            _log_model_with_signature(model, x_test[:1])

            logger.info(f"{run_name} - Test Accuracy: {test_accuracy:.4f}, Test Loss: {test_loss:.4f}")

            return model, history

    except Exception as e:
        logger.error(f"Training failed for {run_name}: {e}")
        raise RuntimeError(f"Training failed: {e}") from e


def _log_training_curves(history: keras.callbacks.History) -> None:
    """
    Create and log training visualization curves.

    Args:
        history: Keras training history object.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Plot loss
    ax1.plot(history.history["loss"], label="Train Loss")
    ax1.plot(history.history["val_loss"], label="Val Loss")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.set_title("Model Loss")
    ax1.legend()
    ax1.grid(True)

    # Plot accuracy
    ax2.plot(history.history["accuracy"], label="Train Accuracy")
    ax2.plot(history.history["val_accuracy"], label="Val Accuracy")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Accuracy")
    ax2.set_title("Model Accuracy")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    mlflow.log_figure(fig, "training_curves.png")
    plt.close()


def _log_model_with_signature(model: keras.Model, input_example: npt.NDArray[np.float32]) -> None:
    """
    Log model to MLflow with signature and input example.

    Args:
        model: Trained Keras model.
        input_example: Example input array for signature inference.
    """
    from mlflow.models.signature import infer_signature

    predictions = model.predict(input_example, verbose=0)
    signature = infer_signature(input_example, predictions)

    mlflow.tensorflow.log_model(
        model,
        "model",
        signature=signature,
        input_example=input_example,
    )


def run_experiments() -> None:
    """Run all three training experiments with different configurations."""
    logger.info("=" * 60)
    logger.info("MNIST MLOps Training Pipeline")
    logger.info("=" * 60)

    # Set MLflow experiment
    mlflow.set_tracking_uri(config.get_mlflow_uri())
    mlflow.set_experiment(config.EXPERIMENT_NAME)

    # Load data
    logger.info("Loading MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = load_mnist_data()

    experiments = [
        {
            "name": "Run_1_Baseline",
            "model_fn": create_baseline_model,
            "config_type": "baseline",
            "description": "Establish baseline performance",
        },
        {
            "name": "Run_2_Improved_Architecture",
            "model_fn": create_improved_architecture_model,
            "config_type": "improved",
            "description": "Add Dropout and increase filters to improve learning",
        },
        {
            "name": "Run_3_Hyperparameter_Tuning",
            "model_fn": create_optimized_model,
            "config_type": "optimized",
            "description": "Optimize convergence with adjusted learning rate and batch size",
        },
    ]

    for exp in experiments:
        logger.info("=" * 60)
        logger.info(f"{exp['name'].upper()}")
        logger.info(f"Purpose: {exp['description']}")
        logger.info("=" * 60)

        model = exp["model_fn"]()
        model_config = get_model_config(exp["config_type"])

        train_model(
            model,
            x_train,
            y_train,
            x_test,
            y_test,
            learning_rate=model_config["learning_rate"],
            batch_size=model_config["batch_size"],
            epochs=model_config["epochs"],
            run_name=exp["name"],
        )

    logger.info("=" * 60)
    logger.info("All experiments completed!")
    logger.info(f"View results at: {config.MLFLOW_TRACKING_URI}")
    logger.info("Run command: mlflow ui")
    logger.info("=" * 60)


def main() -> None:
    """Main entry point for training script."""
    try:
        run_experiments()
    except Exception as e:
        logger.error(f"Training pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()
