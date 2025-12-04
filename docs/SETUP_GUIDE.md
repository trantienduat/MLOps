# MLOps MNIST Project - Setup Guide

## 📋 Complete Setup Checklist

### Phase 1: Environment Setup (30 minutes)

#### 1.1 Install Python 3.11
- [ ] Download Python 3.11 from [python.org](https://www.python.org/downloads/)
- [ ] Verify installation: `python3.11 --version`

#### 1.2 Create Project Environment
```bash
# Create project directory
mkdir MLOps
cd MLOps

# Create virtual environment
python3.11 -m venv .venv

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Verify Python version
python --version  # Should show 3.11.x
```

#### 1.3 Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python scripts/verify_env.py
```

---

### Phase 2: Training & Experiments (1-2 hours)

#### 2.1 Run Training Script
```bash
# Run all three experiments
python src/train.py

# This will:
# - Download MNIST dataset
# - Train 3 different models
# - Log metrics to MLflow
# - Save models
```

Expected output:
- ✓ Run 1: Baseline model (~98% accuracy)
- ✓ Run 2: Improved architecture (~98.5% accuracy)
- ✓ Run 3: Hyperparameter tuning (~99%+ accuracy)

#### 2.2 View Experiments in MLflow
```bash
# Start MLflow UI
mlflow ui

# Open browser to: http://127.0.0.1:5000
```

In MLflow UI:
- [ ] View all three runs
- [ ] Compare metrics (accuracy, loss)
- [ ] View training curves
- [ ] Check model parameters

#### 2.3 Register Best Model
1. [ ] Select the run with highest test_accuracy
2. [ ] Click "Register Model"
3. [ ] Model name: `Mnist_Best_Model`
4. [ ] Version: 1
5. [ ] Transition to: `Production`

---

### Phase 3: Web Application (1-2 hours)

#### 3.1 Test Flask App Locally
```bash
# Run the Flask application
python src/app.py

# Should see:
# - Model loaded successfully!
# - Application running at: http://127.0.0.1:5000
```

#### 3.2 Test Web Interface
1. [ ] Open http://127.0.0.1:5000 in browser
2. [ ] Draw digit "3" on canvas
3. [ ] Click "Predict" button
4. [ ] Verify prediction is correct
5. [ ] Repeat for digits: 5, 7, 0, 9

#### 3.3 Test API Endpoint
```bash
# Health check
curl http://127.0.0.1:5000/health

# Should return: {"model_loaded": true, "status": "healthy"}
```

---

### Phase 4: Docker Setup (1 hour)

#### 4.1 Build Docker Image
```bash
# Build the image
docker build -t mlops-mnist:latest .

# Verify image was created
docker images | grep mlops-mnist
```

#### 4.2 Test Docker Container Locally
```bash
# Run container
docker run -p 5000:5000 mlops-mnist:latest

# Test in browser: http://127.0.0.1:5000
# Test drawing and prediction
```

#### 4.3 Push to Docker Hub
```bash
# Login to Docker Hub
docker login

# Tag image
docker tag mlops-mnist:latest YOUR_USERNAME/mlops-mnist:latest

# Push to Docker Hub
docker push YOUR_USERNAME/mlops-mnist:latest

# Verify on Docker Hub: https://hub.docker.com
```

---

### Phase 5: GitHub & CI/CD (1 hour)

#### 5.1 Create GitHub Repository
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: MLOps MNIST project"

# Create repository on GitHub
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/MLOps.git
git branch -M main
git push -u origin main
```

#### 5.2 Configure GitHub Secrets
1. [ ] Go to: Settings → Secrets and variables → Actions
2. [ ] Click "New repository secret"
3. [ ] Add `DOCKER_USERNAME` (your Docker Hub username)
4. [ ] Add `DOCKER_PASSWORD` (your Docker Hub password or access token)

#### 5.3 Verify CI/CD Pipeline
```bash
# Make a small change
echo "# Update" >> README.md

# Commit and push
git add .
git commit -m "Test CI/CD pipeline"
git push

# Check GitHub Actions tab
# Should see workflow running
```

Workflow should:
- [ ] Checkout code
- [ ] Build Docker image
- [ ] Login to Docker Hub
- [ ] Push image with tags

---

### Phase 6: Documentation & Report (1-2 hours)

#### 6.1 Record Demo Video
Record screen showing:
1. [ ] MLflow UI with 3 experiment runs
2. [ ] Model registry with Production model
3. [ ] GitHub Actions showing successful build
4. [ ] Docker Hub showing pushed image
5. [ ] Web app demo - drawing and predicting digits (3, 5, 7)

Tools:
- Mac: QuickTime Player (Cmd+Shift+5)
- Windows: Xbox Game Bar (Win+G)
- Linux: SimpleScreenRecorder

#### 6.2 Prepare Report Document
Include:
- [ ] Project title and overview
- [ ] Screenshots of each phase
- [ ] Explanation of 3 experimental runs
- [ ] MLflow metrics comparison table
- [ ] Architecture diagrams
- [ ] GitHub repository link
- [ ] Video link (upload to YouTube/Google Drive)
- [ ] Conclusion and learnings

---

## 🎯 Verification Checklist

Before submission, verify:

### Training Phase
- [ ] All 3 runs completed successfully
- [ ] MLflow UI shows all experiments
- [ ] Best model registered in Model Registry
- [ ] Model tagged as "Production"

### Web Application
- [ ] Flask app starts without errors
- [ ] Can draw on canvas
- [ ] Predictions are accurate
- [ ] Clear button works
- [ ] API returns proper JSON

### Docker
- [ ] Image builds successfully
- [ ] Container runs without errors
- [ ] App accessible on port 5000
- [ ] Image pushed to Docker Hub

### CI/CD
- [ ] GitHub repository created
- [ ] Secrets configured
- [ ] Workflow runs successfully (green check)
- [ ] Image auto-pushed to Docker Hub

### Documentation
- [ ] README.md complete
- [ ] Code has comments
- [ ] Report document prepared
- [ ] Video recorded
- [ ] All links working

---

## 🐛 Common Issues & Solutions

### Issue: "Module not found" errors
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: MLflow UI not starting
```bash
# Solution: Check if port 5000 is already in use
lsof -ti:5000 | xargs kill -9
mlflow ui --port 5001
```

### Issue: Model not loading in Flask app
```bash
# Solution: Register model in MLflow first
# 1. Run: python src/train.py
# 2. Open MLflow UI and register best model
# 3. Restart Flask app
```

### Issue: Docker build fails
```bash
# Solution: Clear Docker cache
docker system prune -a
docker build --no-cache -t mlops-mnist .
```

### Issue: GitHub Actions workflow fails
```bash
# Solution: Check secrets are configured correctly
# Verify DOCKER_USERNAME and DOCKER_PASSWORD in Settings
```

---

## 📊 Expected Results

### Model Performance
- **Run 1 (Baseline)**: ~98.0% accuracy
- **Run 2 (Improved)**: ~98.5% accuracy
- **Run 3 (Optimized)**: ~99.0% accuracy

### Training Time
- Each run: ~2-5 minutes (depending on hardware)
- Total training: ~10-15 minutes

### Docker Image Size
- ~1.5-2 GB (includes TensorFlow)

---

## 📞 Support

If you encounter issues:
1. Check this guide thoroughly
2. Review error messages carefully
3. Search for solutions online
4. Check GitHub Issues (if repository is public)

---

**Good luck with your MLOps project! 🚀**
