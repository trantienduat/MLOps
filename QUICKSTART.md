# MLOps Project - Quick Start Guide

This guide will help you get the MLOps project running on your local machine.

## ✅ Prerequisites

- Python 3.11+ (Python 3.12 is supported)
- Git
- 4GB+ RAM
- Internet connection (for downloading dependencies and datasets)

## 🚀 Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/trantienduat/MLOps.git
cd MLOps
```

### Step 2: Run Automated Setup (Recommended)

The easiest way to set up the project:

```bash
./setup.sh
```

This script will:
- ✅ Check Python version
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create .env configuration file
- ✅ Set up pre-commit hooks
- ✅ Create necessary directories

After the script completes, activate the virtual environment:

```bash
source .venv/bin/activate  # On Linux/Mac
# OR
.venv\Scripts\activate     # On Windows
```

### Step 3: Verify Installation

Run the verification script to ensure everything is set up correctly:

```bash
python verify_setup.py
```

This will check:
- ✅ Python version compatibility
- ✅ All required packages installed
- ✅ Project structure intact
- ✅ Environment configuration
- ✅ Module imports working
- ✅ Basic functionality

Expected output:
```
✓ All checks passed! Project is ready to use!
```

## 📊 Training Models

### Option 1: Local Training (with MLflow File Storage)

```bash
# Set environment for local file storage
export PYTHONPATH=/path/to/MLOps
python src/training/train.py
```

This will:
- Download MNIST dataset automatically
- Train 3 different models (baseline, improved, optimized)
- Log all metrics and artifacts to `mlruns/` directory
- Create model files in `mlartifacts/`

### Option 2: Using Docker Compose (Recommended for Production)

```bash
# Start MLflow server
docker-compose up mlflow -d

# Train models (from your host machine)
export MLFLOW_TRACKING_URI=http://localhost:5000
python src/training/train.py

# Or train inside a container
docker-compose run api python src/training/train.py
```

## 📈 Viewing Experiment Results

After training, view results in MLflow UI:

```bash
mlflow ui
```

Then open: http://localhost:5000

You'll see:
- 📊 All experiment runs
- 📈 Training metrics (accuracy, loss)
- 🎯 Model comparisons
- 📁 Artifacts (plots, model files)

## 🎯 Register Best Model

After training, register the best model:

```bash
python scripts/register_model.py
```

This will:
- Find the best performing model
- Register it in MLflow Model Registry
- Tag it for production use

## 🌐 Running the API Server

### Option 1: Development Mode

```bash
# Start the API server
python src/api/main.py

# Or with uvicorn directly
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Access:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Option 2: Production Mode (Docker)

```bash
# First time (required): create experiment runs so fallback can work, and register model for registry-first boot
docker-compose run --rm api python -m src.training.train
printf 'y\n' | docker-compose run --rm api python scripts/register_model.py

# Start all services (MLflow + API)
docker-compose up -d

# Check logs
docker-compose logs -f api

# Stop services
docker-compose down
```

> Want the model baked into the image (no registry at runtime)?
> 1) Copy an MLflow model to `model_store/model` (e.g., `cp -r mlruns/<exp>/<run>/artifacts/model model_store/` or `mlflow models download -m "models:/Mnist_Best_Model/Production" -d model_store/model`).
> 2) `docker build -t mlops-mnist:with-model .`
> 3) `docker-compose up -d` (the API will load `MODEL_LOCAL_PATH` first).

Notes:
- If you skip registration, keep ALLOW_RUN_FALLBACK=true (default) and ensure the experiment `MNIST_Classification_Experiments` exists from the training step above.

## 🧪 Testing the API

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "Mnist_Best_Model",
  "model_version": "1"
}
```

### Make a Prediction

```bash
# Using the web UI
Open http://localhost:8000 in your browser

# Or using curl with base64 encoded image
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/png;base64,iVBORw0KG..."}'
```

### View Metrics

```bash
curl http://localhost:8000/metrics
```

## 🐳 Docker Commands

```bash
# Build the image
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# With monitoring stack (Prometheus + Grafana)
docker-compose --profile monitoring up -d
```

## 🧪 Running Tests

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=html

# Run specific test types
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
pytest tests/e2e/          # End-to-end tests only

# Run with verbose output
pytest -v

# Run and skip slow tests
pytest -m "not slow"
```

View coverage report:
```bash
# Open htmlcov/index.html in your browser
python -m http.server 8080 --directory htmlcov
```

## 🔧 Code Quality Checks

```bash
# Format code
black .
isort .

# Check code quality
flake8 .
pylint src/

# Type checking
mypy src/

# Run all checks at once
pre-commit run --all-files
```

## 🔍 Troubleshooting

### Issue: "Module not found" errors

**Solution**: Set PYTHONPATH
```bash
export PYTHONPATH=/path/to/MLOps
# Or add to .env file
echo "PYTHONPATH=/path/to/MLOps" >> .env
```

### Issue: "Connection refused" to MLflow

**Solution**: Use file-based storage
```bash
# Edit .env file
MLFLOW_TRACKING_URI=file:///absolute/path/to/MLOps/mlruns

# Or start MLflow server
mlflow server --host 0.0.0.0 --port 5000
```

### Issue: MNIST dataset download fails

**Solution**: Manual download or use cached version
```bash
# Check if you're behind a proxy/firewall
# Dataset is cached in: ~/.keras/datasets/mnist.npz

# Or download manually and place in ~/.keras/datasets/
wget https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz \
  -O ~/.keras/datasets/mnist.npz
```

### Issue: "Model not found" when starting API

**Solution**: Train and register a model first
```bash
# Train models
python src/training/train.py

# Register the best one
python scripts/register_model.py
```

### Issue: Port 8000 already in use

**Solution**: Use a different port
```bash
# Edit .env
API_PORT=8080

# Or set environment variable
export API_PORT=8080
python src/api/main.py
```

### Issue: Docker build fails

**Solution**: Check Docker and network
```bash
# Check Docker is running
docker --version
docker ps

# Clean up and rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 📁 Project Structure

```
MLOps/
├── src/
│   ├── api/           # FastAPI application
│   ├── models/        # ML model definitions
│   ├── data/          # Data loading and preprocessing
│   ├── training/      # Training scripts
│   ├── monitoring/    # Metrics and monitoring
│   └── utils/         # Configuration and logging
├── tests/             # Test suite
├── scripts/           # Helper scripts
├── templates/         # Web UI templates
├── mlruns/           # MLflow experiments (local)
├── mlartifacts/      # MLflow artifacts (local)
├── logs/             # Application logs
├── .env              # Environment configuration
└── verify_setup.py   # Setup verification script
```

## 🎓 Learning Resources

- **MLflow**: https://mlflow.org/docs/latest/
- **FastAPI**: https://fastapi.tiangolo.com/
- **TensorFlow**: https://www.tensorflow.org/guide
- **Docker**: https://docs.docker.com/get-started/

## 🆘 Getting Help

1. **Check Documentation**: See `docs/` folder for detailed guides
2. **Run Verification**: `python verify_setup.py`
3. **Check Logs**: Look in `logs/` directory
4. **GitHub Issues**: Report bugs at https://github.com/trantienduat/MLOps/issues

## ✨ Next Steps

After successful setup:

1. ✅ Explore MLflow UI: http://localhost:5000
2. ✅ Try the API: http://localhost:8000/api/docs
3. ✅ Draw digits in the UI: http://localhost:8000
4. ✅ View metrics: http://localhost:8000/metrics
5. ✅ Read the documentation in `docs/`
6. ✅ Modify and experiment with the code

Happy MLOps! 🚀
