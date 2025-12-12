# Enterprise MLOps MNIST Classification System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B%20%7C%203.12-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.17.1-orange.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-green.svg)
![MLflow](https://img.shields.io/badge/MLflow-2.9.2-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Production-ready ML system for MNIST digit recognition following enterprise best practices**

[Quick Start](#quick-start) • [Documentation](docs/) • [API Docs](#api-documentation) • [Contributing](#contributing)

</div>

---

## 🎯 Overview

Enterprise-grade MLOps system demonstrating production best practices:

- ✅ **Experiment Tracking**: MLflow with comprehensive metrics
- ✅ **Model Registry**: Automated model versioning and staging
- ✅ **Production API**: FastAPI with Pydantic validation
- ✅ **Monitoring**: Prometheus metrics and health checks
- ✅ **Testing**: 80%+ code coverage with pytest
- ✅ **Code Quality**: Black, isort, flake8, mypy enforcement
- ✅ **CI/CD**: Comprehensive GitHub Actions pipeline
- ✅ **Security**: Multi-stage Docker, non-root user, dependency scanning
- ✅ **Type Safety**: Full type hints throughout codebase
- ✅ **Observability**: Structured logging and metrics

## 🚀 Quick Start

> **📚 New User?** Check [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions and [STATUS.md](STATUS.md) for known issues and solutions.

### Prerequisites
- Python 3.11+ (Python 3.12 supported and tested)
- Docker & Docker Compose (optional but recommended)
- 4GB+ RAM
- Internet connection (for dependencies and datasets)

### Option 1: Automated Setup (Recommended)
```bash
git clone https://github.com/trantienduat/MLOps.git
cd MLOps
./setup.sh
source .venv/bin/activate

# Verify installation
python verify_setup.py
```

### Option 2: Manual Setup
```bash
# Clone repository
git clone https://github.com/trantienduat/MLOps.git
cd MLOps

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration
```

### Start the MLflow Tracking Server

The training pipeline requires an MLflow server listening on port 5000 so that every experiment run is tracked. Start it before running `src/training/train.py`:

```bash
mlflow server \
   --backend-store-uri file://$PWD/mlruns \
   --default-artifact-root file://$PWD/mlruns \
   --host 0.0.0.0 \
   --port 5000
```

Leave that terminal/session running while the training runs below execute.

### Train Models
```bash
# Set PYTHONPATH (important!)
export PYTHONPATH=$(pwd)

# Run training pipeline (creates 3 experiments)
python src/training/train.py

# View results in MLflow UI
mlflow ui
# Open http://localhost:5000
```

> **Note**: If MNIST dataset download fails due to network restrictions, see [STATUS.md](STATUS.md#2-mnist-dataset-download-issues) for solutions.

### Start API Server

#### Development Mode
```bash
uvicorn src.api.main:app --reload
# API: http://localhost:8000
# Docs: http://localhost:8000/api/docs
```

#### Production Mode (Docker)
```bash
# First time (required): create experiment runs so fallback can work, and register model for registry-first boot
docker-compose run --rm api python -m src.training.train
printf 'y\n' | docker-compose run --rm api python scripts/register_model.py

# Start all services (MLflow + API)
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Health check
curl http://localhost:8000/health

# Notes
# - If you skip registration, keep ALLOW_RUN_FALLBACK=true (default) and ensure the experiment 'MNIST_Classification_Experiments' exists from the training step above.
# - Compose mounts ./mlruns and ./mlartifacts to persist runs/artifacts on the host.
# - MLflow listens on 0.0.0.0:5000 inside compose; access via http://localhost:5000 on the host.

# Optional: bake model into the image (no registry needed at runtime)
# 1) Export a model into model_store/model (MLflow format)
#    cp -r mlruns/<experiment_id>/<run_id>/artifacts/model model_store/
#    # or download a registered model version:
#    mlflow models download -m "models:/Mnist_Best_Model/Production" -d model_store/model
# 2) Build image (MODEL_LOCAL_PATH defaults to /app/model_store/model)
#    docker build -t mlops-mnist:with-model .
# 3) Run compose (will load baked model first)
#    docker-compose up -d
```

## 📁 Project Structure

```
MLOps/
├── .github/
│   ├── workflows/
│   │   └── docker-image.yml     # CI/CD pipeline
│   └── copilot-instructions.md  # Development guidelines
├── src/
│   ├── api/                     # FastAPI application
│   │   ├── main.py             # API endpoints
│   │   └── schemas.py          # Pydantic models
│   ├── models/                  # Model architectures
│   │   └── cnn.py              # CNN models
│   ├── data/                    # Data processing
│   │   └── loader.py           # MNIST loader
│   ├── training/                # Training pipeline
│   │   └── train.py            # Training script
│   ├── monitoring/              # Observability
│   │   └── metrics.py          # Prometheus metrics
│   └── utils/                   # Utilities
│       ├── config.py           # Configuration
│       └── logger.py           # Logging setup
├── tests/                       # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
├── docs/                        # Documentation
├── templates/                   # Web UI
├── scripts/                     # Helper scripts
├── .env.example                # Environment template
├── .pre-commit-config.yaml     # Pre-commit hooks
├── pyproject.toml              # Project configuration
├── docker-compose.yml          # Local orchestration
├── Dockerfile                  # Multi-stage build
└── requirements.txt            # Dependencies
```

## 🔬 ML Development Workflow

### Experiment Strategy

**Baseline → Iterate → Optimize → Deploy**

```bash
# All experiments tracked in MLflow
python src/training/train.py
```

| Run | Purpose | Architecture | Hyperparameters | Expected Accuracy |
|-----|---------|--------------|-----------------|-------------------|
| 1 | Baseline | 1 Conv2D, 1 Dense | LR=0.001, BS=128, E=5 | ~98% |
| 2 | Architecture | + Dropout, 64 filters | LR=0.001, BS=128, E=5 | ~98.5% |
| 3 | Optimization | Same as Run 2 | LR=0.0005, BS=64, E=5 | ~99%+ |

**View Results**: `mlflow ui` → http://localhost:5000

## 🌐 API Documentation

### Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```
Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "Mnist_Best_Model",
  "model_version": "1"
}
```

#### Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/png;base64,..."}'
```
Response:
```json
{
  "prediction": 5,
  "confidence": 0.9876,
  "probabilities": [0.001, 0.002, ..., 0.9876, ...]
}
```

#### Interactive API Docs
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Monitoring

#### Prometheus Metrics
```bash
curl http://localhost:8000/metrics
```

Available metrics:
- `predictions_total` - Total predictions by class
- `prediction_latency_seconds` - Request latency histogram
- `prediction_confidence` - Model confidence gauge
- `api_requests_total` - API request count by endpoint
- `active_requests` - Currently active requests

## 🧪 Testing

### Run Tests

```bash
# All tests with coverage
pytest --cov=src --cov-report=html

# Specific test types
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/e2e/          # End-to-end tests

# With markers
pytest -m "not slow"       # Skip slow tests
pytest -v                  # Verbose output
```

### Code Quality

```bash
# Format code
black .
isort .

# Lint
flake8 .
pylint src/

# Type check
mypy src/

# All checks (pre-commit)
pre-commit run --all-files
```

### Coverage Report
After running tests, open `htmlcov/index.html` for detailed coverage report.

## 🐳 Docker & Deployment

### Local Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

### Production Deployment

```bash
# Build production image
docker build -t mlops-mnist:v1.0.0 .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e MLFLOW_TRACKING_URI=http://mlflow-server:5000 \
  -e MODEL_NAME=Mnist_Best_Model \
  mlops-mnist:v1.0.0

# Check health
docker ps
curl http://localhost:8000/health
```

### Monitoring Stack (Optional)

```bash
# Start with Prometheus & Grafana
docker-compose --profile monitoring up -d

# Access services
# - API: http://localhost:8000
# - MLflow: http://localhost:5000
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

Automated on every push to `main`:

1. **Lint Stage**
   - Black formatting check
   - isort import sorting
   - Flake8 style guide
   - MyPy type checking

2. **Test Stage**
   - Unit tests with coverage
   - Integration tests
   - Coverage upload to Codecov

3. **Security Stage**
   - Safety dependency scan
   - pip-audit vulnerability check

4. **Build & Push Stage**
   - Multi-stage Docker build
   - Push to Docker Hub
   - Tag with SHA and latest
   - Trivy security scan

### Setup CI/CD

1. Add GitHub Secrets:
   ```
   DOCKER_USERNAME: your-dockerhub-username
   DOCKER_PASSWORD: your-dockerhub-token
   ```

2. Push to trigger:
   ```bash
   git push origin main
   ```

3. Monitor: `Actions` tab in GitHub repo

## 📚 Documentation

Comprehensive technical documentation:

- **[Architecture](docs/ARCHITECTURE.md)** - System architecture with C4 diagrams
- **[ML Pipeline](docs/ML_PIPELINE.md)** - Model training and experimentation
- **[API Documentation](docs/API.md)** - REST API reference and examples
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment strategies

## 🛠️ Development

### Project Guidelines

See [`.github/copilot-instructions.md`](.github/copilot-instructions.md) for:
- Coding standards (PEP 8, type hints, docstrings)
- Architecture patterns (microservices, API-first)
- Security best practices
- Testing requirements (80% coverage)
- MLOps workflow (baseline → optimize → deploy)

### Adding New Features

1. Create feature branch: `git checkout -b feature/your-feature`
2. Write tests first (TDD)
3. Implement feature with type hints and docstrings
4. Run linting: `pre-commit run --all-files`
5. Run tests: `pytest --cov=src`
6. Create pull request

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- TensorFlow & Keras teams for ML framework
- MLflow for experiment tracking
- FastAPI for modern API framework
- Docker for containerization

---

<div align="center">

**Built with ❤️ using Enterprise MLOps Best Practices**

[⬆ Back to Top](#enterprise-mlops-mnist-classification-system)

</div>

---

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- MNIST Dataset: Yann LeCun et al.
- MLflow: Databricks
- TensorFlow: Google Brain
- FastAPI: Sebastián Ramírez

---

**For detailed technical information, architecture diagrams, and deployment guides, see the [documentation](docs/).**
