# ⚠️ IMPORTANT: Installation Notes

## Before Running Any Scripts

The project requires TensorFlow and other dependencies to be installed in a virtual environment.

### First-Time Setup

```bash
# 1. Create virtual environment with Python 3.11
python3.11 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install all dependencies
pip install -r requirements.txt
```

### Verification

After installation, run:

```bash
python scripts/test_setup.py
```

You should see:
```
✅ All required packages are installed!
✅ Training Script - PASS
✅ Flask Application - PASS
```

### Common Installation Issues

#### Issue: "ModuleNotFoundError: No module named 'tensorflow'"
**Solution**: Activate virtual environment and install dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: "No module named 'tensorflow.keras'"
**Solution**: This is normal if TensorFlow isn't installed. The code has fallback imports.
Just install TensorFlow:
```bash
pip install tensorflow==2.15.0
```

#### Issue: Package installation fails on Apple Silicon (M1/M2/M3)
**Solution**: Use conda or install with specific flags
```bash
# Option 1: Use conda
conda install tensorflow

# Option 2: Use pip with flags
pip install tensorflow-macos==2.15.0
pip install tensorflow-metal  # For GPU acceleration
```

#### Issue: "Permission denied" when installing packages
**Solution**: Don't use sudo. Use virtual environment:
```bash
# Create fresh virtual environment
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Verify Installation

```bash
# Check TensorFlow
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"

# Check MLflow
python -c "import mlflow; print('MLflow version:', mlflow.__version__)"

# Check Flask
python -c "import flask; print('Flask version:', flask.__version__)"

# Run complete test
python scripts/test_setup.py
```

### Expected Output

After successful installation:
- TensorFlow version: 2.15.0
- MLflow version: 2.9.2
- Flask version: 3.0.0
- All tests: PASS

---

## ✅ Once Installed Successfully

You can then run:

```bash
# Train models
python src/train.py

# Start MLflow UI  
mlflow ui

# Run web app
python src/app.py

# Or run complete pipeline
./run_pipeline.sh       # Mac/Linux
run_pipeline.bat        # Windows
```

---

## 📦 Requirements File Contents

Current `requirements.txt`:
```
tensorflow==2.15.0
mlflow==2.9.2
flask==3.0.0
numpy==1.24.4
matplotlib==3.7.4
scikit-learn==1.3.2
scipy==1.11.4
pillow==10.1.0
```

All versions are tested and compatible with Python 3.11.

---

## 🆘 Still Having Issues?

1. **Delete and recreate virtual environment**:
   ```bash
   rm -rf venv
   python3.11 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Check Python version**:
   ```bash
   python --version  # Should be 3.9, 3.10, or 3.11
   ```

3. **Clear pip cache**:
   ```bash
   pip cache purge
   pip install --no-cache-dir -r requirements.txt
   ```

4. **Install packages one by one**:
   ```bash
   pip install tensorflow==2.15.0
   pip install mlflow==2.9.2
   pip install flask==3.0.0
   # ... etc
   ```

---

**Remember**: Always activate your virtual environment before running any scripts!

```bash
source venv/bin/activate  # You should see (venv) in your terminal prompt
```
