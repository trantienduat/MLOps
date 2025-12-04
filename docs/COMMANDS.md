# MLOps MNIST - Command Cheat Sheet

## Quick Reference for All Commands

---

## 🔧 Environment Setup

```bash
# Create virtual environment
python3.11 -m venv .venv

# Activate virtual environment
source .venv/bin/activate          # Mac/Linux
.venv\Scripts\activate             # Windows

# Deactivate virtual environment
deactivate

# Install dependencies
pip install -r requirements.txt

# Update pip
pip install --upgrade pip

# Verify environment
python scripts/test_setup.py
python scripts/verify_env.py
```

---

## 🎓 Training Commands

```bash
# Train all 3 models with MLflow tracking
python src/train.py

# View training progress (logs will show in terminal)

# Expected duration: 10-15 minutes
```

---

## 📊 MLflow Commands

```bash
# Start MLflow UI (default port 5000)
mlflow ui

# Start on different port
mlflow ui --port 5001

# Start with specific backend store
mlflow ui --backend-store-uri ./mlruns

# View experiments
# Open browser: http://127.0.0.1:5000

# Stop MLflow UI
# Press Ctrl+C in terminal
```

---

## 🤖 Model Registration

```bash
# Automatic registration (recommended)
python scripts/register_model.py

# Manual registration
# 1. Open MLflow UI
# 2. Select best run
# 3. Click "Register Model"
# 4. Name: Mnist_Best_Model
# 5. Stage: Production
```

---

## 🌐 Web Application

```bash
# Run Flask app (default port 5000)
python src/app.py

# Note: Stop MLflow UI first if using port 5000

# Access web app
# Open browser: http://127.0.0.1:5000

# Stop Flask app
# Press Ctrl+C in terminal
```

---

## 🐳 Docker Commands

```bash
# Build Docker image
docker build -t mlops-mnist:latest .

# Build without cache
docker build --no-cache -t mlops-mnist:latest .

# Run Docker container
docker run -p 5000:5000 mlops-mnist:latest

# Run in detached mode
docker run -d -p 5000:5000 mlops-mnist:latest

# Run with custom name
docker run -d -p 5000:5000 --name mnist-app mlops-mnist:latest

# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop mnist-app

# Remove container
docker rm mnist-app

# List images
docker images

# Remove image
docker rmi mlops-mnist:latest

# Tag image for Docker Hub
docker tag mlops-mnist:latest YOUR_USERNAME/mlops-mnist:latest

# Login to Docker Hub
docker login

# Push to Docker Hub
docker push YOUR_USERNAME/mlops-mnist:latest

# Pull from Docker Hub
docker pull YOUR_USERNAME/mlops-mnist:latest

# Clean up Docker
docker system prune -a           # Remove all unused data
docker image prune               # Remove unused images
docker container prune           # Remove stopped containers
```

---

## 📦 Git Commands

```bash
# Initialize repository
git init

# Check status
git status

# Add all files
git add .

# Add specific file
git add filename.py

# Commit changes
git commit -m "Your commit message"

# View commit history
git log
git log --oneline

# Create new branch
git branch feature-name

# Switch branch
git checkout branch-name
git switch branch-name           # Newer syntax

# Create and switch to new branch
git checkout -b feature-name

# Add remote repository
git remote add origin https://github.com/USERNAME/MLOps.git

# View remotes
git remote -v

# Push to remote
git push origin main

# Push and set upstream
git push -u origin main

# Pull from remote
git pull origin main

# View differences
git diff

# Undo changes (not staged)
git checkout -- filename.py

# Unstage file
git reset HEAD filename.py

# View branches
git branch
git branch -a                    # All branches including remote
```

---

## 🔍 Debugging Commands

```bash
# Check Python version
python --version

# Check if in virtual environment
which python                     # Should show path to .venv

# List installed packages
pip list
pip freeze

# Check for package
pip show tensorflow

# Find process using port
lsof -ti:5000                    # Mac/Linux
netstat -ano | findstr :5000     # Windows

# Kill process on port
lsof -ti:5000 | xargs kill -9    # Mac/Linux
# Windows: Use Task Manager

# View file contents
cat filename.py                  # Mac/Linux
type filename.py                 # Windows

# Search for text in files
grep -r "search_term" .          # Mac/Linux
findstr /s "search_term" *.*     # Windows

# Check disk space
df -h                            # Mac/Linux
dir                              # Windows
```

---

## 🧪 Testing Commands

```bash
# Run environment test
python scripts/test_setup.py

# Run quick start guide
python scripts/quick_start.py

# Test model registration
python scripts/register_model.py

# Run complete pipeline
./run_pipeline.sh                # Mac/Linux
run_pipeline.bat                 # Windows

# Test API with curl
curl http://127.0.0.1:5000/health

curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_data_here"}'
```

---

## 📁 File Operations

```bash
# Create directory
mkdir directory_name

# Create file
touch filename.py                # Mac/Linux
type nul > filename.py           # Windows

# Copy file
cp source.py destination.py      # Mac/Linux
copy source.py destination.py    # Windows

# Move/rename file
mv old_name.py new_name.py       # Mac/Linux
move old_name.py new_name.py     # Windows

# Delete file
rm filename.py                   # Mac/Linux
del filename.py                  # Windows

# Delete directory
rm -rf directory_name            # Mac/Linux
rmdir /s directory_name          # Windows

# View file size
ls -lh filename.py               # Mac/Linux
dir filename.py                  # Windows
```

---

## 🎬 Complete Workflow

```bash
# 1. Setup
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/test_setup.py

# 2. Train
python src/train.py

# 3. Register Model
mlflow ui                        # In one terminal
python scripts/register_model.py         # In another terminal

# 4. Test Web App
python src/app.py
# Draw and test in browser

# 5. Docker
docker build -t mlops-mnist .
docker run -p 5000:5000 mlops-mnist

# 6. GitHub
git add .
git commit -m "Complete MLOps project"
git push origin main

# 7. Verify CI/CD
# Check GitHub Actions tab
# Check Docker Hub for image
```

---

## 🆘 Common Issues

```bash
# Issue: Port already in use
lsof -ti:5000 | xargs kill -9

# Issue: Virtual environment not activated
source .venv/bin/activate

# Issue: Module not found
pip install -r requirements.txt

# Issue: Docker build fails
docker system prune -a
docker build --no-cache -t mlops-mnist .

# Issue: Git conflicts
git status
git stash
git pull
git stash pop

# Issue: MLflow tracking server not found
mlflow ui --backend-store-uri ./mlruns
```

---

## 💡 Productivity Tips

```bash
# Create alias for common commands (add to ~/.zshrc or ~/.bashrc)
alias venv='source .venv/bin/activate'
alias mlflow-ui='mlflow ui'
alias run-app='python src/app.py'
alias run-train='python src/train.py'

# Use tab completion
python t[TAB]                    # Autocompletes to train.py

# View command history
history
history | grep docker

# Repeat last command
!!

# Run previous command with sudo
sudo !!
```

---

## 📚 Help Commands

```bash
# Python help
python --help
python -m pip --help

# MLflow help
mlflow --help
mlflow ui --help

# Docker help
docker --help
docker run --help
docker build --help

# Git help
git --help
git commit --help
```

---

**Quick tip**: Bookmark this file for easy reference during development!
