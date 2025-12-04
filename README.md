# MLOps MNIST Digit Recognition Project

📚 **Full documentation is available in [`docs/README.md`](docs/README.md)**

## Quick Start

```bash
# 1. Setup environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Train models
python src/train.py

# 3. View experiments
mlflow ui

# 4. Register best model
python scripts/register_model.py

# 5. Run web app
python src/app.py
```

## Project Structure

```
MLOps/
├── docs/               # All documentation and guides
├── scripts/            # Helper scripts (test, register, pipeline)
├── src/                # Source code (train.py, app.py)
├── templates/          # Frontend HTML
├── .github/workflows/  # CI/CD configuration
├── requirements.txt    # Python dependencies
└── Dockerfile         # Container configuration
```

## Documentation

- **[README](docs/README.md)** - Complete project documentation
- **[Getting Started](docs/GETTING_STARTED.md)** - Quick 5-minute setup
- **[Setup Guide](docs/SETUP_GUIDE.md)** - Detailed setup with checklists
- **[Installation](docs/INSTALLATION.md)** - Install dependencies & troubleshooting
- **[Commands](docs/COMMANDS.md)** - Command reference cheat sheet
- **[Project Summary](docs/PROJECT_SUMMARY.md)** - Implementation status
- **[Index](docs/INDEX.md)** - Documentation navigator

## Quick Commands

```bash
# Run complete pipeline (Unix/Mac)
./scripts/run_pipeline.sh

# Run complete pipeline (Windows)
scripts\run_pipeline.bat

# Test environment
python scripts/test_setup.py

# Verify packages
python scripts/verify_env.py
```

For detailed instructions, see [`docs/README.md`](docs/README.md).
│   └── index.html              # Web UI
├── mlruns/                     # MLflow tracking data
├── train.py                    # Training script with 3 runs
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── README.md                   # This file
└── verify_env.py              # Environment verification
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11
- pip
- (Optional) Docker for containerization

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd MLOps
   ```

2. **Create virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Phase 1: Training & Experimentation

### Run Training Pipeline

Execute the training script to run all three experiments:

```bash
python train.py
```

This will create three runs:
- **Run 1 (Baseline)**: Simple CNN with 1 Conv2D layer
- **Run 2 (Improved Architecture)**: Added Dropout and increased filters
- **Run 3 (Hyperparameter Tuning)**: Optimized learning rate and batch size

### View Experiments in MLflow UI

```bash
mlflow ui
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### Register Best Model

1. Open MLflow UI
2. Compare runs by metrics (accuracy, loss)
3. Select the best performing run
4. Click "Register Model"
5. Name: `Mnist_Best_Model`
6. Stage: `Production`

## 🌐 Phase 2: Web Application

### Run Flask App Locally

```bash
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) to:
- Draw digits on the canvas
- Get real-time predictions
- View confidence scores for all digits

### API Endpoints

- `GET /` - Web UI
- `POST /predict` - Prediction API
  ```json
  {
    "image": "base64_encoded_image_data"
  }
  ```
- `GET /health` - Health check

## 🐳 Phase 3: Docker Deployment

### Build Docker Image

```bash
docker build -t mlops-mnist:latest .
```

### Run Container

```bash
docker run -p 5000:5000 mlops-mnist:latest
```

### Push to Docker Hub

```bash
docker tag mlops-mnist:latest <your-dockerhub-username>/mlops-mnist:latest
docker push <your-dockerhub-username>/mlops-mnist:latest
```

## 🔄 Phase 4: CI/CD with GitHub Actions

### Setup

1. **Create Docker Hub account** and repository `mlops-mnist`

2. **Configure GitHub Secrets**:
   - Go to: `Settings → Secrets and variables → Actions`
   - Add secrets:
     - `DOCKER_USERNAME`: Your Docker Hub username
     - `DOCKER_PASSWORD`: Your Docker Hub password/token

3. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial MLOps project setup"
   git push origin main
   ```

### Automatic Deployment

Every push to `main` branch will:
1. Trigger GitHub Actions workflow
2. Build Docker image
3. Push to Docker Hub
4. Tag with `latest` and commit SHA

Monitor builds at: `https://github.com/<username>/MLOps/actions`

## 📈 Experiment Results

### Run Comparison

| Run | Architecture | Hyperparameters | Test Accuracy |
|-----|-------------|-----------------|---------------|
| 1 | Baseline (1 Conv2D) | LR=0.001, BS=128 | ~98% |
| 2 | + Dropout, More Filters | LR=0.001, BS=128 | ~98.5% |
| 3 | Same as Run 2 | LR=0.0005, BS=64 | ~99%+ |

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
