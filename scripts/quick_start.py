"""
Quick start script to help users get started with the MLOps project.
"""

import sys
import os


def print_banner():
    """Print welcome banner."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "🚀 MLOps MNIST Project - Quick Start 🚀" + " " * 19 + "║")
    print("╚" + "=" * 78 + "╝")
    print()


def print_section(title):
    """Print section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def main():
    """Display quick start guide."""
    print_banner()

    print("Welcome to the MLOps MNIST Digit Recognition project!")
    print("This guide will help you get started quickly.\n")

    # Check if in virtual environment
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )

    if not in_venv:
        print("⚠️  Warning: You don't appear to be in a virtual environment.")
        print("   It's recommended to use a virtual environment.\n")

    print_section("📋 PHASE 1: SETUP (First Time Only)")
    print(
        """
1. Create and activate virtual environment:
   
   python3.11 -m venv venv
   source venv/bin/activate  # Mac/Linux
   # OR
   venv\\Scripts\\activate  # Windows

2. Install dependencies:
   
   pip install -r requirements.txt

3. Verify installation:
   
   python test_setup.py
    """
    )

    print_section("🎓 PHASE 2: TRAIN MODELS")
    print(
        """
Run the training script to create 3 experiment runs:

   python train.py

This will:
- Download MNIST dataset (first time only)
- Train 3 different models with various architectures
- Log metrics and models to MLflow
- Take ~10-15 minutes to complete

Expected results:
- Run 1 (Baseline):        ~98.0% accuracy
- Run 2 (Architecture):    ~98.5% accuracy  
- Run 3 (Hyperparameter):  ~99.0% accuracy
    """
    )

    print_section("📊 PHASE 3: VIEW EXPERIMENTS")
    print(
        """
Start MLflow UI to view and compare experiments:

   mlflow ui

Then:
1. Open browser to: http://127.0.0.1:5000
2. View all 3 experiment runs
3. Compare metrics and visualizations
4. Select best model (highest test_accuracy)
5. Register model:
   - Click "Register Model"
   - Name: Mnist_Best_Model
   - Stage: Production
    """
    )

    print_section("🌐 PHASE 4: RUN WEB APPLICATION")
    print(
        """
Start the Flask web application:

   python app.py

Then:
1. Open browser to: http://127.0.0.1:5000
2. Draw a digit (0-9) on the canvas
3. Click "Predict" to see AI prediction
4. View confidence scores
5. Try different digits!

Note: Make sure MLflow UI is stopped first (uses same port 5000)
or run MLflow on different port: mlflow ui --port 5001
    """
    )

    print_section("🐳 PHASE 5: DOCKER (BONUS)")
    print(
        """
Build and run with Docker:

   # Build image
   docker build -t mlops-mnist:latest .
   
   # Run container
   docker run -p 5000:5000 mlops-mnist:latest
   
   # Push to Docker Hub (optional)
   docker tag mlops-mnist:latest YOUR_USERNAME/mlops-mnist:latest
   docker push YOUR_USERNAME/mlops-mnist:latest
    """
    )

    print_section("🔄 PHASE 6: CI/CD WITH GITHUB ACTIONS (BONUS)")
    print(
        """
1. Create GitHub repository
2. Configure secrets in GitHub:
   Settings → Secrets → Actions
   - DOCKER_USERNAME
   - DOCKER_PASSWORD

3. Push code:
   
   git add .
   git commit -m "MLOps project complete"
   git push origin main

4. Check Actions tab for automated builds
    """
    )

    print_section("📚 USEFUL COMMANDS")
    print(
        """
# Check environment
python test_setup.py

# Train models
python train.py

# View experiments
mlflow ui

# Run web app
python app.py

# Run tests
python -m pytest  # If tests are added

# Docker commands
docker build -t mlops-mnist .
docker run -p 5000:5000 mlops-mnist

# Git commands
git add .
git commit -m "Update"
git push
    """
    )

    print_section("📖 DOCUMENTATION")
    print(
        """
- README.md         - Complete project documentation
- SETUP_GUIDE.md    - Detailed setup instructions
- .github/copilot-instructions.md - Project requirements
    """
    )

    print_section("🆘 TROUBLESHOOTING")
    print(
        """
Common issues:

1. "Module not found":
   → pip install -r requirements.txt

2. "Port 5000 already in use":
   → lsof -ti:5000 | xargs kill -9

3. "Model not found":
   → Run python train.py first
   → Register model in MLflow UI

4. Docker build fails:
   → docker system prune -a
   → docker build --no-cache -t mlops-mnist .
    """
    )

    print("\n" + "=" * 80)
    print("✨ Ready to start? Run: python test_setup.py")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
