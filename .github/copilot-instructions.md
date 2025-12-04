# Enterprise MLOps Project - Development Guidelines

> **Mission**: Build production-ready ML systems following industry best practices and enterprise standards.

---

## 🎯 PROJECT PHILOSOPHY

### Core Principles

1. **Reproducibility First**: All experiments must be 100% reproducible
2. **Automation by Default**: Manual processes are technical debt
3. **Observability Everywhere**: If you can't measure it, you can't improve it
4. **Security by Design**: Never compromise on security for convenience
5. **Scalability from Start**: Design for growth, not just current needs

---

## 🏗️ ARCHITECTURE STANDARDS

### System Design Requirements

- **Microservices Architecture**: Separate concerns (training, serving, monitoring)
- **Event-Driven Design**: Use message queues for async operations
- **API-First Development**: RESTful APIs with OpenAPI/Swagger specs
- **Container Native**: Everything must be containerized
- **Cloud Agnostic**: Avoid vendor lock-in where possible

### Technology Stack

- **Python Version**: Python 3.11+ (use `.venv` for virtual environments)
- **ML Framework**: TensorFlow 2.15+ or PyTorch 2.0+
- **Experiment Tracking**: MLflow with remote tracking server
- **Model Registry**: MLflow Model Registry with stage transitions
- **API Framework**: FastAPI (preferred) or Flask with Gunicorn
- **Container Runtime**: Docker with multi-stage builds
- **Orchestration**: Kubernetes (production) or Docker Compose (development)

---

## 📋 CODING STANDARDS

### Python Conventions (PEP 8 + Enterprise Extensions)

```python
# Naming Conventions
- snake_case: variables, functions, methods, modules
- PascalCase: classes, type aliases
- UPPER_SNAKE_CASE: constants, environment variables
- _leading_underscore: private/internal methods

# File Organization
- __init__.py: Package initialization only
- config.py: Configuration classes/constants
- schemas.py: Pydantic models, data classes
- utils.py: Helper functions (keep small, split if >200 lines)
```

### Mandatory Practices

- ✅ **Type Hints**: Use typing for all function signatures
- ✅ **Docstrings**: Google style for all public functions/classes
- ✅ **Error Handling**: Explicit exceptions, never bare `except:`
- ✅ **Logging**: Use `logging` module, structured logs (JSON in production)
- ✅ **Configuration**: Environment-based, never hardcode credentials
- ✅ **Testing**: Minimum 80% code coverage
- ✅ **Linting**: Black, isort, flake8, mypy in pre-commit hooks

### Code Quality Tools

```bash
# Required in requirements-dev.txt
black==23.12.1           # Code formatting
isort==5.13.2            # Import sorting
flake8==7.0.0            # Style guide enforcement
mypy==1.8.0              # Static type checking
pylint==3.0.3            # Code analysis
pytest==7.4.4            # Testing framework
pytest-cov==4.1.0        # Coverage reporting
pre-commit==3.6.0        # Git hooks
```

---

## 🔬 ML DEVELOPMENT WORKFLOW

### 1. Experiment Management (MLflow)

```python
# MANDATORY: Every training run must be tracked
import mlflow
from mlflow.tracking import MlflowClient

# Set up remote tracking server (not localhost)
mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("mnist-classification")

with mlflow.start_run(run_name="baseline-cnn-v1") as run:
    # Log parameters
    mlflow.log_params({
        "model_architecture": "cnn",
        "optimizer": "adam",
        "learning_rate": 0.001,
        "batch_size": 32,
        "epochs": 10
    })
    
    # Log metrics per epoch
    for epoch in range(epochs):
        mlflow.log_metrics({
            "train_loss": train_loss,
            "train_accuracy": train_acc,
            "val_loss": val_loss,
            "val_accuracy": val_acc
        }, step=epoch)
    
    # Log model with signature
    mlflow.tensorflow.log_model(
        model, 
        "model",
        signature=signature,
        input_example=input_example
    )
    
    # Log artifacts
    mlflow.log_artifacts("plots/", artifact_path="visualizations")
```

### 2. Model Development Strategy

**Baseline → Iterate → Optimize → Deploy**

#### Run 1: Baseline (Essential)
- Simple architecture (1-2 layers)
- Default hyperparameters
- Fast iteration (low epochs)
- **Purpose**: Establish performance floor

#### Run 2: Architecture Tuning
- Add complexity (layers, units, dropout)
- Regularization techniques
- Data augmentation
- **Purpose**: Find optimal model structure

#### Run 3: Hyperparameter Optimization
- Grid search or Bayesian optimization
- Learning rate scheduling
- Batch size tuning
- **Purpose**: Maximize performance

#### Run 4+: Production Candidate
- Cross-validation
- Ensemble methods
- Model compression (quantization, pruning)
- **Purpose**: Production-ready model

### 3. Model Registry & Lifecycle

```python
# Register best model
client = MlflowClient()
model_uri = f"runs:/{run_id}/model"
model_name = "mnist-classifier"

# Register with metadata
result = mlflow.register_model(
    model_uri=model_uri,
    name=model_name,
    tags={
        "task": "image-classification",
        "framework": "tensorflow",
        "version": "1.0.0"
    }
)

# Transition through stages: None → Staging → Production → Archived
client.transition_model_version_stage(
    name=model_name,
    version=result.version,
    stage="Staging"  # Then "Production" after validation
)
```

---

## 🌐 API DEVELOPMENT (FastAPI)

### Structure

```python
# src/api/main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import numpy as np

app = FastAPI(
    title="MNIST Prediction API",
    version="1.0.0",
    docs_url="/api/docs"
)

# Request/Response schemas
class PredictionRequest(BaseModel):
    image: list[list[float]] = Field(..., description="28x28 image array")
    
    class Config:
        json_schema_extra = {
            "example": {
                "image": [[0.0] * 28 for _ in range(28)]
            }
        }

class PredictionResponse(BaseModel):
    prediction: int
    confidence: float
    probabilities: list[float]

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        # Load model (use singleton pattern in production)
        model = load_model_from_registry()
        
        # Preprocess
        image = np.array(request.image).reshape(1, 28, 28, 1)
        
        # Predict
        probabilities = model.predict(image)[0]
        prediction = int(np.argmax(probabilities))
        confidence = float(probabilities[prediction])
        
        return PredictionResponse(
            prediction=prediction,
            confidence=confidence,
            probabilities=probabilities.tolist()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Production Deployment

```bash
# Use Gunicorn with Uvicorn workers
gunicorn src.api.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
```

---

## 🐳 CONTAINERIZATION (Docker)

### Multi-Stage Dockerfile

```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

# Security: Run as non-root
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

# Environment
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    MLFLOW_TRACKING_URI=http://mlflow:5000

USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["gunicorn", "src.api.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

---

## 🔄 CI/CD PIPELINE (GitHub Actions)

### .github/workflows/ml-pipeline.yml

```yaml
name: ML Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Lint
        run: |
          black --check .
          isort --check .
          flake8 .
          mypy .
      
      - name: Test
        run: pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build-and-push:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/mlops-mnist:latest
            ${{ secrets.DOCKER_USERNAME }}/mlops-mnist:${{ github.sha }}
          cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/mlops-mnist:buildcache
          cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/mlops-mnist:buildcache,mode=max

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: |
          # Add deployment logic (Kubernetes, AWS ECS, etc.)
          echo "Deploy to staging environment"
```

---

## 📊 MONITORING & OBSERVABILITY

### Application Monitoring

```python
# src/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
prediction_counter = Counter(
    'predictions_total', 
    'Total number of predictions',
    ['model_version', 'prediction_class']
)

prediction_latency = Histogram(
    'prediction_latency_seconds',
    'Time spent processing prediction'
)

model_confidence = Gauge(
    'prediction_confidence',
    'Model confidence score'
)

# Use in API
@prediction_latency.time()
def predict(image):
    result = model.predict(image)
    prediction = int(np.argmax(result))
    confidence = float(result[0][prediction])
    
    prediction_counter.labels(
        model_version='1.0.0',
        prediction_class=str(prediction)
    ).inc()
    
    model_confidence.set(confidence)
    
    return result
```

### Model Performance Monitoring

```python
# Track model drift
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def monitor_data_drift(reference_data, current_data):
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data)
    report.save_html('reports/drift_report.html')
    
    # Alert if drift detected
    if report.as_dict()['metrics'][0]['result']['dataset_drift']:
        send_alert("Data drift detected!")
```

---

## 🔒 SECURITY BEST PRACTICES

### Secrets Management

```bash
# NEVER commit secrets to Git
# Use environment variables or secret managers

# .env (add to .gitignore)
MLFLOW_TRACKING_URI=http://mlflow:5000
DATABASE_URL=postgresql://user:pass@host:5432/db
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...

# Use python-dotenv
from dotenv import load_dotenv
load_dotenv()
```

### Dependency Security

```bash
# Add to CI/CD pipeline
pip install safety
safety check

# OR
pip install pip-audit
pip-audit
```

### Container Security

```dockerfile
# Scan images
docker scan mlops-mnist:latest

# Use minimal base images
FROM gcr.io/distroless/python3-debian11

# Run as non-root (already shown above)
```

---

## 📁 PROJECT STRUCTURE (Enterprise Standard)

```
mlops-mnist/
├── .github/
│   ├── workflows/
│   │   ├── ml-pipeline.yml
│   │   ├── docker-image.yml
│   │   └── security-scan.yml
│   └── copilot-instructions.md
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes/
│   │   └── schemas.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── cnn.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   └── preprocessing.py
│   ├── training/
│   │   ├── __init__.py
│   │   ├── train.py
│   │   └── evaluate.py
│   ├── monitoring/
│   │   ├── __init__.py
│   │   └── metrics.py
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/
│   ├── register_model.py
│   ├── deploy.sh
│   └── setup_env.sh
├── docs/
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── ARCHITECTURE.md
├── notebooks/
│   └── exploratory/
├── mlruns/
├── .venv/
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── docker-compose.yml
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── setup.py
└── README.md
```

---

## ✅ DEFINITION OF DONE

### For Each Feature

- [ ] Code passes all linting checks (black, isort, flake8, mypy)
- [ ] Unit tests written with ≥80% coverage
- [ ] Integration tests pass
- [ ] API documentation updated (OpenAPI/Swagger)
- [ ] Logging and monitoring instrumented
- [ ] Security scan passes (no critical vulnerabilities)
- [ ] Code reviewed and approved
- [ ] CI/CD pipeline green
- [ ] Documentation updated

### For Model Deployment

- [ ] Model performance meets acceptance criteria
- [ ] A/B testing completed (if applicable)
- [ ] Model card created (model details, performance, limitations)
- [ ] Monitoring dashboards configured
- [ ] Rollback plan documented
- [ ] Production deployment approved by stakeholders

---

## 🚀 QUICK START (Enterprise Setup)

```bash
# 1. Clone and setup
git clone https://github.com/USERNAME/MLOps.git
cd MLOps
python3.11 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Setup pre-commit hooks
pre-commit install

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 5. Run tests
pytest

# 6. Start development environment
docker-compose up -d

# 7. Train model
python src/training/train.py

# 8. Start API
uvicorn src.api.main:app --reload
```

---

## 📚 ADDITIONAL RESOURCES

- [MLOps Principles](https://ml-ops.org/)
- [Google's ML Best Practices](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [AWS Well-Architected ML Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html)
- [MLflow Best Practices](https://mlflow.org/docs/latest/tracking.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Remember**: Enterprise MLOps is not just about ML models—it's about building reliable, scalable, and maintainable ML systems.

