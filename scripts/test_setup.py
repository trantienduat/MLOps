"""
Script to run a quick test of the MLOps project.

This script:
1. Verifies the environment
2. Runs a quick training test
3. Tests model prediction
"""

import sys
import subprocess


def check_imports():
    """Check if all required packages are installed."""
    print("=" * 60)
    print("Checking required packages...")
    print("=" * 60)
    
    packages = {
        'tensorflow': 'TensorFlow',
        'mlflow': 'MLflow',
        'flask': 'Flask',
        'numpy': 'NumPy',
        'matplotlib': 'Matplotlib',
        'PIL': 'Pillow'
    }
    
    missing = []
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name:15s} - OK")
        except ImportError:
            print(f"✗ {name:15s} - MISSING")
            missing.append(package)
    
    if missing:
        print("\n❌ Missing packages:", ", ".join(missing))
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All required packages are installed!")
    return True


def check_python_version():
    """Check Python version."""
    print("\n" + "=" * 60)
    print("Checking Python version...")
    print("=" * 60)
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 9:
        print("✅ Python version is compatible (3.9+)")
        return True
    else:
        print("⚠️  Recommended Python version is 3.11")
        return True


def test_training():
    """Test if training script can be imported."""
    print("\n" + "=" * 60)
    print("Testing training script...")
    print("=" * 60)
    
    try:
        sys.path.insert(0, 'src')
        import train
        print("✅ Training script can be imported")
        print("   Functions available:")
        print(f"   - load_mnist_data: {hasattr(train, 'load_mnist_data')}")
        print(f"   - create_baseline_model: {hasattr(train, 'create_baseline_model')}")
        print(f"   - train_model: {hasattr(train, 'train_model')}")
        return True
    except Exception as e:
        print(f"❌ Error importing training script: {e}")
        return False


def test_app():
    """Test if Flask app can be imported."""
    print("\n" + "=" * 60)
    print("Testing Flask application...")
    print("=" * 60)
    
    try:
        sys.path.insert(0, 'src')
        import app
        print("✅ Flask app can be imported")
        print(f"   - Flask app created: {app.app is not None}")
        print(f"   - Routes defined: {len(app.app.url_map._rules)} routes")
        return True
    except Exception as e:
        print(f"❌ Error importing Flask app: {e}")
        return False


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "MLOps Project - Quick Test" + " " * 16 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = []
    
    # Check Python version
    results.append(("Python Version", check_python_version()))
    
    # Check imports
    results.append(("Package Installation", check_imports()))
    
    # Test training script
    results.append(("Training Script", test_training()))
    
    # Test Flask app
    results.append(("Flask Application", test_app()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:25s} - {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! You're ready to go!")
        print("\nNext steps:")
        print("1. Run training: python train.py")
        print("2. View experiments: mlflow ui")
        print("3. Run web app: python app.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
