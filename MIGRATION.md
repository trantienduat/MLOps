# Migration Guide - Enterprise Refactor

This document guides you through migrating from the old structure to the new enterprise architecture.

## 🔄 Major Changes

### Directory Structure
```
OLD → NEW
train.py → src/training/train.py
app.py → src/api/main.py (Flask → FastAPI)
verify_env.py → scripts/verify_env.py
test_setup.py → scripts/test_setup.py
```

### Code Organization
- **Data Loading**: Moved to `src/data/loader.py`
- **Models**: Moved to `src/models/cnn.py`
- **Configuration**: Centralized in `src/utils/config.py`
- **Logging**: Centralized in `src/utils/logger.py`
- **Monitoring**: New `src/monitoring/metrics.py`

### API Changes
- **Framework**: Flask → FastAPI
- **Port**: 5000 → 8000 (configurable)
- **Docs**: Auto-generated at `/api/docs`
- **Schema Validation**: Pydantic models
- **Metrics**: Prometheus endpoint at `/metrics`

## 📝 Breaking Changes

### 1. Training Script
**OLD**:
```bash
python train.py
```

**NEW**:
```bash
python src/training/train.py
```

### 2. API Server
**OLD**:
```bash
python app.py
# Runs on port 5000
```

**NEW**:
```bash
python src/api/main.py
# Or: uvicorn src.api.main:app --reload
# Runs on port 8000
```

### 3. Environment Variables
**OLD**: Hardcoded values in code

**NEW**: Environment-based configuration
```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Docker
**OLD**: Single-stage, runs as root

**NEW**: Multi-stage, non-root user
```dockerfile
# Now uses gunicorn + uvicorn workers
# Health checks included
# Smaller image size
```

### 5. Dependencies
**NEW PACKAGES**:
- `fastapi` - Modern API framework
- `uvicorn` - ASGI server
- `gunicorn` - Production server
- `pydantic` - Data validation
- `python-dotenv` - Environment management
- `prometheus-client` - Metrics

**REMOVED**:
- `flask` - Replaced by FastAPI

## 🚀 Migration Steps

### Step 1: Backup Current Work
```bash
git add .
git commit -m "Backup before enterprise refactor"
```

### Step 2: Install New Dependencies
```bash
# Deactivate old venv if active
deactivate

# Remove old virtual environment
rm -rf venv

# Create new .venv
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Step 3: Setup Environment
```bash
cp .env.example .env
# Edit .env with your MLflow URI, model name, etc.
```

### Step 4: Setup Development Tools
```bash
pre-commit install
```

### Step 5: Retrain Models (Optional)
```bash
# Old models are still in mlruns/
# But you can retrain with new code:
python src/training/train.py
```

### Step 6: Register Model
```bash
python scripts/register_model.py
```

### Step 7: Test New API
```bash
# Development mode
uvicorn src.api.main:app --reload

# Visit http://localhost:8000/api/docs
```

### Step 8: Run Tests
```bash
pytest --cov=src
```

### Step 9: Format Code
```bash
black .
isort .
flake8 .
```

## 🔧 Configuration Migration

### MLflow Configuration
**OLD**: Used default localhost:5000

**NEW**: Configurable via .env
```bash
MLFLOW_TRACKING_URI=http://localhost:5000
MODEL_NAME=Mnist_Best_Model
EXPERIMENT_NAME=MNIST_Classification_Experiments
```

### API Configuration
**NEW**: All configurable
```bash
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
LOG_LEVEL=INFO
ENVIRONMENT=development
```

## 📊 Testing Migration

### Old Tests
```bash
python scripts/test_setup.py
python scripts/verify_env.py
```

### New Tests
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests with coverage
pytest --cov=src --cov-report=html
```

## 🐳 Docker Migration

### Old Docker Workflow
```bash
docker build -t mlops-mnist .
docker run -p 5000:5000 mlops-mnist
```

### New Docker Workflow
```bash
# Using docker-compose (recommended)
docker-compose up -d

# Or standalone
docker build -t mlops-mnist .
docker run -p 8000:8000 mlops-mnist

# With monitoring
docker-compose --profile monitoring up -d
```

## 📚 Updated Commands

| Task | Old Command | New Command |
|------|-------------|-------------|
| Train | `python train.py` | `python src/training/train.py` |
| API | `python app.py` | `uvicorn src.api.main:app --reload` |
| MLflow UI | `mlflow ui` | `mlflow ui` (same) |
| Register | `python scripts/register_model.py` | `python scripts/register_model.py` (same) |
| Test | `python scripts/test_setup.py` | `pytest` |
| Docker Build | `docker build -t mlops-mnist .` | `docker build -t mlops-mnist .` (different Dockerfile) |
| Docker Run | `docker run -p 5000:5000 mlops-mnist` | `docker-compose up -d` |

## 🎯 Benefits of Migration

✅ **Type Safety**: Full type hints + MyPy
✅ **Testing**: 80%+ code coverage with pytest
✅ **Code Quality**: Black, isort, flake8 enforcement
✅ **API**: FastAPI with auto-docs and validation
✅ **Monitoring**: Prometheus metrics
✅ **Security**: Non-root Docker, dependency scanning
✅ **CI/CD**: Comprehensive GitHub Actions pipeline
✅ **Logging**: Structured logging with levels
✅ **Configuration**: Environment-based setup
✅ **Documentation**: Auto-generated API docs

## 🆘 Troubleshooting

### Import Errors
```bash
# Ensure virtual environment is activated
which python  # Should show .venv

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Conflicts
```bash
# Old API might still be running on 5000
lsof -ti:5000 | xargs kill -9

# New API uses 8000
lsof -ti:8000 | xargs kill -9
```

### Model Not Found
```bash
# Check MLflow tracking URI
mlflow ui

# Re-register model
python scripts/register_model.py
```

### Docker Issues
```bash
# Clean rebuild
docker-compose down
docker system prune -a
docker-compose up -d --build
```

## 📞 Need Help?

- Check updated documentation in `docs/`
- Review [QUICKSTART.md](QUICKSTART.md)
- See [.github/copilot-instructions.md](.github/copilot-instructions.md)
- Open an issue on GitHub

---

**The migration preserves all your MLflow experiments and trained models while upgrading to enterprise standards.**
