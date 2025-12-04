# Quick Start Guide - Enterprise MLOps MNIST

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/trantienduat/MLOps.git
cd MLOps
```

### 2. Setup Virtual Environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (for testing & linting)
pip install -r requirements-dev.txt
```

### 4. Setup Pre-commit Hooks (Optional)
```bash
pre-commit install
```

### 5. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Training Models

```bash
# Run training pipeline (creates 3 experiments)
python src/training/train.py

# View results in MLflow UI
mlflow ui
# Open http://localhost:5000
```

## Running the API

### Option 1: Local Development
```bash
# Using uvicorn (development)
uvicorn src.api.main:app --reload --port 8000

# Or using the app directly
python src/api/main.py
```

### Option 2: Docker Compose (Recommended)
```bash
# Start all services (MLflow + API)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 3: Production Docker
```bash
# Build image
docker build -t mlops-mnist:latest .

# Run container
docker run -p 8000:8000 mlops-mnist:latest
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test types
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
pytest -m "not slow"        # Skip slow tests
```

## Code Quality

```bash
# Format code
black .
isort .

# Lint code
flake8 .
pylint src/

# Type checking
mypy src/

# Run all checks
pre-commit run --all-files
```

## API Endpoints

- **Health Check**: `GET http://localhost:8000/health`
- **Prediction**: `POST http://localhost:8000/predict`
- **API Docs**: `GET http://localhost:8000/api/docs`
- **Metrics**: `GET http://localhost:8000/metrics`
- **Web UI**: `GET http://localhost:8000/`

## Monitoring (Optional)

```bash
# Start with monitoring stack
docker-compose --profile monitoring up -d

# Access services
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)
```

## Project Structure

```
MLOps/
├── src/
│   ├── api/           # FastAPI application
│   ├── models/        # Model architectures
│   ├── data/          # Data loaders
│   ├── training/      # Training pipeline
│   ├── monitoring/    # Prometheus metrics
│   └── utils/         # Config & logging
├── tests/             # Test suite
├── docs/              # Documentation
├── templates/         # Web UI
└── mlruns/           # MLflow experiments
```

## Common Issues

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Model Not Found
Ensure you've trained models and registered them in MLflow:
```bash
python src/training/train.py
python scripts/register_model.py
```

### Import Errors
Ensure virtual environment is activated:
```bash
which python  # Should show .venv path
```

## Next Steps

1. Train models: `python src/training/train.py`
2. Register best model: `python scripts/register_model.py`
3. Start API: `docker-compose up -d`
4. Test prediction: Visit `http://localhost:8000`
5. View metrics: `http://localhost:8000/metrics`

## Documentation

- [Full README](docs/README.md)
- [Installation Guide](docs/INSTALLATION.md)
- [Commands Reference](docs/COMMANDS.md)
- [API Documentation](http://localhost:8000/api/docs) (when running)

## Support

For issues or questions, please open an issue on GitHub.
