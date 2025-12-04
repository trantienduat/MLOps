# 📚 MLOps MNIST Project - Documentation Index

Welcome to the MLOps MNIST project! This index helps you find the right documentation for your needs.

---

## 🚀 I Want To...

### Get Started Quickly
👉 **[GETTING_STARTED.md](GETTING_STARTED.md)** - Quick 5-minute setup guide

### Understand the Project
👉 **[README.md](README.md)** - Complete project overview and documentation

### Set Up Step-by-Step
👉 **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed installation and setup instructions

### Install Dependencies
👉 **[INSTALLATION.md](INSTALLATION.md)** - Dependency installation and troubleshooting

### Find Commands
👉 **[COMMANDS.md](COMMANDS.md)** - Complete command reference and cheat sheet

### Review Project Status
👉 **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Implementation summary and checklist

---

## 📁 File Guide

### 🎯 Main Application Files

| File | Purpose |
|------|---------|
| `train.py` | Training script with 3 experimental runs |
| `app.py` | Flask web application for predictions |
| `templates/index.html` | Web UI with drawing canvas |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Docker container configuration |

### 🛠️ Helper Scripts

| Script | Purpose |
|--------|---------|
| `test_setup.py` | Verify environment and installation |
| `verify_env.py` | Check Python environment |
| `quick_start.py` | Interactive quick start guide |
| `register_model.py` | Auto-register best model to MLflow |
| `run_pipeline.sh` | Complete pipeline runner (Mac/Linux) |
| `run_pipeline.bat` | Complete pipeline runner (Windows) |

### 📖 Documentation Files

| Document | What's Inside |
|----------|---------------|
| **GETTING_STARTED.md** | Quick start (5 min setup) |
| **README.md** | Full project documentation |
| **SETUP_GUIDE.md** | Detailed setup with checklists |
| **INSTALLATION.md** | Install guide + troubleshooting |
| **COMMANDS.md** | Command reference cheat sheet |
| **PROJECT_SUMMARY.md** | Implementation status |
| **INDEX.md** | This file - documentation navigator |

### ⚙️ Configuration Files

| File | Purpose |
|------|---------|
| `.github/workflows/docker-image.yml` | GitHub Actions CI/CD |
| `.dockerignore` | Docker build exclusions |
| `.gitignore` | Git exclusions |
| `.github/copilot-instructions.md` | Project requirements |

---

## 🎯 Quick Navigation by Task

### First Time Setup
1. Read → [GETTING_STARTED.md](GETTING_STARTED.md)
2. Install → [INSTALLATION.md](INSTALLATION.md)
3. Verify → Run `python test_setup.py`

### Training Models
1. Prerequisites → [INSTALLATION.md](INSTALLATION.md#verify-installation)
2. Run → `python train.py`
3. View → `mlflow ui`
4. Register → `python register_model.py`

### Running Web App
1. Setup → [GETTING_STARTED.md](GETTING_STARTED.md#step-5-run-web-app-1-minute)
2. Run → `python app.py`
3. Test → Draw digits at http://127.0.0.1:5000

### Docker Deployment
1. Guide → [README.md](README.md#-phase-3-docker-deployment)
2. Build → `docker build -t mlops-mnist .`
3. Run → `docker run -p 5000:5000 mlops-mnist`

### CI/CD Setup
1. Guide → [SETUP_GUIDE.md](SETUP_GUIDE.md#phase-5-github--cicd-1-hour)
2. Configure → GitHub Secrets
3. Deploy → Push to main branch

### Troubleshooting
1. Installation → [INSTALLATION.md](INSTALLATION.md#common-installation-issues)
2. General → [README.md](README.md#-troubleshooting)
3. Commands → [COMMANDS.md](COMMANDS.md#-common-issues)

---

## 📊 Documentation Levels

### 🟢 Beginner - Start Here
1. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Friendly introduction
2. **[INSTALLATION.md](INSTALLATION.md)** - Step-by-step setup
3. Run `python quick_start.py` - Interactive guide

### 🟡 Intermediate - Deep Dive
1. **[README.md](README.md)** - Complete documentation
2. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed procedures
3. **[COMMANDS.md](COMMANDS.md)** - Command reference

### 🔴 Advanced - Implementation Details
1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical summary
2. `.github/copilot-instructions.md` - Requirements spec
3. Source code - `train.py`, `app.py`

---

## 🔍 Find Information By Topic

### Environment & Installation
- Quick setup: [GETTING_STARTED.md](GETTING_STARTED.md#-super-quick-start-automated)
- Detailed install: [INSTALLATION.md](INSTALLATION.md)
- Troubleshooting: [INSTALLATION.md](INSTALLATION.md#common-installation-issues)

### Training & Experiments
- Overview: [README.md](README.md#-phase-1-training--experimentation)
- 3 Run details: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md#12-training--experiment-code-)
- MLflow setup: [SETUP_GUIDE.md](SETUP_GUIDE.md#22-view-experiments-in-mlflow)

### Web Application
- Quick test: [GETTING_STARTED.md](GETTING_STARTED.md#step-5-run-web-app-1-minute)
- Features: [README.md](README.md#-phase-2-web-application)
- API docs: [README.md](README.md#api-endpoints)

### Docker & Deployment
- Docker guide: [README.md](README.md#-phase-3-docker-deployment)
- Commands: [COMMANDS.md](COMMANDS.md#-docker-commands)
- Checklist: [SETUP_GUIDE.md](SETUP_GUIDE.md#phase-4-docker-setup-1-hour)

### CI/CD
- GitHub Actions: [README.md](README.md#-phase-4-cicd-with-github-actions)
- Setup: [SETUP_GUIDE.md](SETUP_GUIDE.md#phase-5-github--cicd-1-hour)
- Workflow file: `.github/workflows/docker-image.yml`

### Commands & Reference
- All commands: [COMMANDS.md](COMMANDS.md)
- Workflow: [COMMANDS.md](COMMANDS.md#-complete-workflow)
- Troubleshooting: [COMMANDS.md](COMMANDS.md#-common-issues)

---

## 🎓 Learning Path

### Day 1: Setup & Understanding
- [ ] Read [GETTING_STARTED.md](GETTING_STARTED.md)
- [ ] Follow [INSTALLATION.md](INSTALLATION.md)
- [ ] Run `python test_setup.py`
- [ ] Read [README.md](README.md) overview

### Day 2: Training & Experiments
- [ ] Run `python train.py`
- [ ] Explore MLflow UI
- [ ] Read about 3 runs in [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- [ ] Register best model

### Day 3: Web Application
- [ ] Run `python app.py`
- [ ] Test predictions
- [ ] Explore code in `app.py`
- [ ] Read API documentation

### Day 4: Docker & Deployment
- [ ] Build Docker image
- [ ] Run container
- [ ] Push to Docker Hub
- [ ] Read [README.md](README.md#-phase-3-docker-deployment)

### Day 5: CI/CD & Automation
- [ ] Setup GitHub repository
- [ ] Configure secrets
- [ ] Push code
- [ ] Watch automated build

---

## 💡 Pro Tips

### For Quick Answers
- **Commands**: Check [COMMANDS.md](COMMANDS.md)
- **Errors**: See [INSTALLATION.md](INSTALLATION.md#common-installation-issues)
- **Steps**: Follow [GETTING_STARTED.md](GETTING_STARTED.md)

### For Deep Understanding
- **Architecture**: Read [README.md](README.md)
- **Implementation**: Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **Requirements**: See `.github/copilot-instructions.md`

### For Specific Tasks
- **First time**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **Training**: Section in [README.md](README.md#-phase-1-training--experimentation)
- **Web app**: Section in [README.md](README.md#-phase-2-web-application)
- **Docker**: Section in [README.md](README.md#-phase-3-docker-deployment)

---

## 📞 Help & Support

### I'm Stuck!
1. Check [INSTALLATION.md](INSTALLATION.md#-still-having-issues) troubleshooting
2. Review [COMMANDS.md](COMMANDS.md#-common-issues)
3. Read error-specific sections in [README.md](README.md#-troubleshooting)

### I Need Command Reference
👉 **[COMMANDS.md](COMMANDS.md)** - Complete command cheat sheet

### I Want Detailed Steps
👉 **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Step-by-step with checklists

---

## 🎯 One-Page Quick Reference

```bash
# Setup (once)
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Train
python train.py

# View experiments
mlflow ui

# Register model
python register_model.py

# Run web app
python app.py

# Docker
docker build -t mlops-mnist .
docker run -p 5000:5000 mlops-mnist

# Full pipeline
./run_pipeline.sh  # Mac/Linux
run_pipeline.bat   # Windows
```

For more details on any command, see [COMMANDS.md](COMMANDS.md)

---

## ✅ Documentation Checklist

Before starting, make sure you have:
- [ ] Read [GETTING_STARTED.md](GETTING_STARTED.md)
- [ ] Followed [INSTALLATION.md](INSTALLATION.md)
- [ ] Verified setup with `python test_setup.py`

During development:
- [ ] Use [COMMANDS.md](COMMANDS.md) as reference
- [ ] Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) checklists
- [ ] Check [README.md](README.md) for details

For submission:
- [ ] Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- [ ] Complete all checklist items
- [ ] Test everything works

---

## 📚 All Documentation Files

1. **[INDEX.md](INDEX.md)** (this file) - Documentation navigator
2. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Quick start (5 min)
3. **[README.md](README.md)** - Main documentation
4. **[INSTALLATION.md](INSTALLATION.md)** - Setup & troubleshooting
5. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed guide with checklists
6. **[COMMANDS.md](COMMANDS.md)** - Command reference
7. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Implementation status

---

**Start here**: [GETTING_STARTED.md](GETTING_STARTED.md) 🚀

**Questions?** Check [INSTALLATION.md](INSTALLATION.md) or [README.md](README.md)

**Need commands?** See [COMMANDS.md](COMMANDS.md)

**Happy Learning!** 🎓
