# Enterprise MLOps MNIST Classification System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15+-orange.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![MLflow](https://img.shields.io/badge/MLflow-2.9+-blue.svg)
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

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional but recommended)

### Option 1: Automated Setup (Recommended)
```bash
git clone https://github.com/trantienduat/MLOps.git
cd MLOps
./setup.sh
source .venv/bin/activate
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

### Train Models
```bash
# Run training pipeline (creates 3 experiments)
python src/training/train.py

# View results in MLflow UI
mlflow ui
# Open http://localhost:5000
```

### Start API Server

#### Development Mode
```bash
uvicorn src.api.main:app --reload
# API: http://localhost:8000
# Docs: http://localhost:8000/api/docs
```

#### Production Mode (Docker)
```bash
# Start all services (MLflow + API)
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
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

Full documentation available in `docs/`:

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[Getting Started](docs/GETTING_STARTED.md)** - Quick 5-minute tutorial
- **[Commands Reference](docs/COMMANDS.md)** - All CLI commands
- **[Setup Guide](docs/SETUP_GUIDE.md)** - Step-by-step checklist
- **[Project Summary](docs/PROJECT_SUMMARY.md)** - Implementation status

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

**Reasoning:**
- **Run 1**: Establishes baseline performance
- **Run 2**: Dropout prevents overfitting, more filters capture complex patterns
- **Run 3**: Smaller learning rate and batch size improve convergence

## 🧪 Testing

### Test the Web Application

1. Open [http://127.0.0.1:5000](http://127.0.0.1:5000)
2. Draw digits: 3, 5, 7
3. Click "Predict"
4. Verify predictions are correct

### Test the API

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_image_data"}'
```

## 📝 Documentation

### Training Parameters

**Run 1 - Baseline:**
- Layers: Conv2D(32) → MaxPool → Dense(10)
- Epochs: 5
- Learning Rate: 0.001
- Batch Size: 128

**Run 2 - Architecture Improvement:**
- Layers: Conv2D(64) → MaxPool → Dropout(0.25) → Dense(128) → Dropout(0.5) → Dense(10)
- Epochs: 5
- Learning Rate: 0.001
- Batch Size: 128

**Run 3 - Hyperparameter Tuning:**
- Same architecture as Run 2
- Epochs: 5
- Learning Rate: 0.0005 (reduced)
- Batch Size: 64 (smaller)

## 🐛 Troubleshooting

### Model Not Loading
```bash
# Train models first
python train.py

# Then register the best model in MLflow UI
mlflow ui
```

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
python app.py --port 8000
```

### Docker Build Issues
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t mlops-mnist .
```

## 📚 Learning Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [TensorFlow Guide](https://www.tensorflow.org/guide)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🎓 Project Highlights

This project demonstrates:
1. **Experiment Tracking**: Systematic comparison of model architectures
2. **Model Registry**: Version control and staging for ML models
3. **MLOps Best Practices**: Reproducibility, versioning, automation
4. **Full-Stack ML**: From training to deployment
5. **DevOps Integration**: CI/CD for ML applications

## 📄 License

This project is created for educational purposes.

## 👤 Author

Created as part of MLOps learning curriculum.

## 🙏 Acknowledgments

- MNIST Dataset: Yann LeCun et al.
- MLflow: Databricks
- TensorFlow: Google

---

**Happy Learning! 🚀**
