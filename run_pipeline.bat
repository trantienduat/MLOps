@echo off
REM MLOps MNIST Project - Complete Pipeline Runner (Windows)
REM This script runs the entire MLOps pipeline from start to finish

echo ========================================
echo MLOps MNIST - Complete Pipeline
echo ========================================
echo.

REM Step 1: Check environment
echo ========================================
echo Step 1: Checking Environment
echo ========================================
echo.
python test_setup.py
if errorlevel 1 (
    echo Error: Environment check failed
    exit /b 1
)
echo [OK] Environment check passed
echo.

REM Step 2: Run training
echo ========================================
echo Step 2: Training Models
echo This may take 10-15 minutes...
echo ========================================
echo.
python train.py
if errorlevel 1 (
    echo Error: Training failed
    exit /b 1
)
echo [OK] Training completed
echo.

REM Step 3: Register best model
echo ========================================
echo Step 3: Registering Best Model
echo ========================================
echo.
python register_model.py
echo.

REM Step 4: Information
echo ========================================
echo Pipeline Complete!
echo ========================================
echo.
echo All steps completed successfully!
echo.
echo Next steps:
echo 1. View experiments:
echo    mlflow ui
echo    Then open: http://127.0.0.1:5000
echo.
echo 2. Run web application:
echo    python app.py
echo    Then open: http://127.0.0.1:5000
echo.
echo 3. Build Docker image:
echo    docker build -t mlops-mnist .
echo.
echo 4. Run with Docker:
echo    docker run -p 5000:5000 mlops-mnist
echo.
pause
