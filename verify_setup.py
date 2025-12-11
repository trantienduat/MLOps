#!/usr/bin/env python3
"""
Comprehensive Project Verification Script

This script verifies that the MLOps project is correctly set up and ready to run.
It checks:
- Python version
- Required packages installation
- Environment configuration
- Required directories
- Module imports
- Basic functionality
"""

import os
import sys
from pathlib import Path
from typing import Tuple, List


class Colors:
    """ANSI color codes for terminal output."""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.RESET}\n")


def print_section(text: str) -> None:
    """Print a section title."""
    print(f"\n{Colors.BOLD}{text}{Colors.RESET}")
    print("-" * 70)


def print_success(text: str) -> None:
    """Print success message."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")


def print_error(text: str) -> None:
    """Print error message."""
    print(f"{Colors.RED}✗{Colors.RESET} {text}")


def print_warning(text: str) -> None:
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {text}")


def check_python_version() -> Tuple[bool, str]:
    """
    Check if Python version is compatible.

    Returns:
        Tuple of (success, message)
    """
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major == 3 and version.minor >= 11:
        return True, f"Python {version_str} (Compatible: 3.11+)"
    else:
        return False, f"Python {version_str} (Required: 3.11+)"


def check_packages() -> Tuple[bool, List[str]]:
    """
    Check if all required packages are installed.

    Returns:
        Tuple of (all_installed, missing_packages)
    """
    required_packages = {
        "tensorflow": "TensorFlow",
        "mlflow": "MLflow",
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "pydantic": "Pydantic",
        "numpy": "NumPy",
        "matplotlib": "Matplotlib",
        "PIL": "Pillow",
        "sklearn": "scikit-learn",
        "prometheus_client": "Prometheus Client",
        "dotenv": "python-dotenv",
    }

    missing = []
    installed = []

    for package, name in required_packages.items():
        try:
            __import__(package)
            installed.append(name)
            print_success(f"{name:20s} - Installed")
        except ImportError:
            missing.append(name)
            print_error(f"{name:20s} - MISSING")

    return len(missing) == 0, missing


def check_dev_packages() -> Tuple[bool, List[str]]:
    """
    Check if development packages are installed.

    Returns:
        Tuple of (all_installed, missing_packages)
    """
    dev_packages = {
        "black": "Black",
        "isort": "isort",
        "flake8": "Flake8",
        "mypy": "MyPy",
        "pytest": "pytest",
    }

    missing = []
    installed = []

    for package, name in dev_packages.items():
        try:
            __import__(package)
            installed.append(name)
            print_success(f"{name:20s} - Installed")
        except ImportError:
            missing.append(name)
            print_warning(f"{name:20s} - MISSING (Optional)")

    return len(missing) == 0, missing


def check_directories() -> Tuple[bool, List[str]]:
    """
    Check if required directories exist.

    Returns:
        Tuple of (all_exist, missing_directories)
    """
    required_dirs = [
        "src",
        "src/api",
        "src/models",
        "src/data",
        "src/training",
        "src/monitoring",
        "src/utils",
        "tests",
        "templates",
        "scripts",
        "docs",
    ]

    optional_dirs = ["mlruns", "mlartifacts", "logs"]

    missing = []

    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print_success(f"{dir_path:30s} - Exists")
        else:
            missing.append(dir_path)
            print_error(f"{dir_path:30s} - MISSING")

    for dir_path in optional_dirs:
        if Path(dir_path).exists():
            print_success(f"{dir_path:30s} - Exists")
        else:
            print_warning(f"{dir_path:30s} - Will be created automatically")

    return len(missing) == 0, missing


def check_files() -> Tuple[bool, List[str]]:
    """
    Check if required files exist.

    Returns:
        Tuple of (all_exist, missing_files)
    """
    required_files = [
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml",
        "setup.sh",
        "Dockerfile",
        "docker-compose.yml",
        ".env.example",
        "src/api/main.py",
        "src/training/train.py",
        "src/utils/config.py",
        "src/utils/logger.py",
    ]

    optional_files = [".env", ".pre-commit-config.yaml"]

    missing = []

    for file_path in required_files:
        if Path(file_path).exists():
            print_success(f"{file_path:40s} - Exists")
        else:
            missing.append(file_path)
            print_error(f"{file_path:40s} - MISSING")

    for file_path in optional_files:
        if Path(file_path).exists():
            print_success(f"{file_path:40s} - Exists")
        else:
            print_warning(f"{file_path:40s} - MISSING (Optional)")

    return len(missing) == 0, missing


def check_environment_config() -> Tuple[bool, str]:
    """
    Check environment configuration.

    Returns:
        Tuple of (configured, message)
    """
    if Path(".env").exists():
        return True, ".env file exists"
    else:
        return False, ".env file not found (copy from .env.example)"


def check_module_imports() -> Tuple[bool, List[str]]:
    """
    Check if project modules can be imported.

    Returns:
        Tuple of (all_import, failed_imports)
    """
    modules = [
        "src.utils.config",
        "src.utils.logger",
        "src.api.schemas",
        "src.models.cnn",
        "src.data.loader",
        "src.monitoring.metrics",
    ]

    failed = []

    for module in modules:
        try:
            __import__(module)
            print_success(f"{module:40s} - OK")
        except Exception as e:
            failed.append(module)
            print_error(f"{module:40s} - FAILED: {str(e)[:50]}")

    return len(failed) == 0, failed


def test_basic_functionality() -> Tuple[bool, str]:
    """
    Test basic functionality.

    Returns:
        Tuple of (success, message)
    """
    try:
        # Test data loading
        from src.data.loader import load_mnist_data

        print_success("Data loader can be imported")

        # Test model creation
        from src.models.cnn import create_baseline_model

        print_success("Model creation can be imported")

        # Test configuration
        from src.utils.config import config

        config.validate()
        print_success("Configuration validation passed")

        return True, "Basic functionality tests passed"
    except Exception as e:
        return False, f"Basic functionality test failed: {str(e)}"


def create_missing_directories() -> None:
    """Create missing optional directories."""
    optional_dirs = ["mlruns", "mlartifacts", "logs"]

    created = []
    for dir_path in optional_dirs:
        path = Path(dir_path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created.append(dir_path)

    if created:
        print_success(f"Created directories: {', '.join(created)}")


def main() -> int:
    """
    Run all verification checks.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print_header("MLOps Project Verification")

    results = {}

    # Python version check
    print_section("1. Python Version")
    success, message = check_python_version()
    results["Python Version"] = success
    if success:
        print_success(message)
    else:
        print_error(message)

    # Package check
    print_section("2. Required Packages")
    success, missing = check_packages()
    results["Required Packages"] = success
    if not success:
        print_error(f"Missing packages: {', '.join(missing)}")
        print_warning("Run: pip install -r requirements.txt")

    # Dev package check
    print_section("3. Development Packages (Optional)")
    dev_success, dev_missing = check_dev_packages()
    if not dev_success:
        print_warning(f"Missing dev packages: {', '.join(dev_missing)}")
        print_warning("Run: pip install -r requirements-dev.txt")

    # Directory check
    print_section("4. Project Structure")
    success, missing = check_directories()
    results["Project Structure"] = success
    if not success:
        print_error(f"Missing directories: {', '.join(missing)}")

    # Create optional directories
    create_missing_directories()

    # File check
    print_section("5. Required Files")
    success, missing = check_files()
    results["Required Files"] = success
    if not success:
        print_error(f"Missing files: {', '.join(missing)}")

    # Environment check
    print_section("6. Environment Configuration")
    success, message = check_environment_config()
    results["Environment Config"] = success
    if success:
        print_success(message)
    else:
        print_warning(message)
        print_warning("Run: cp .env.example .env")

    # Module import check
    print_section("7. Module Imports")
    success, failed = check_module_imports()
    results["Module Imports"] = success
    if not success:
        print_error(f"Failed imports: {', '.join(failed)}")

    # Basic functionality check
    print_section("8. Basic Functionality")
    success, message = test_basic_functionality()
    results["Basic Functionality"] = success
    if success:
        print_success(message)
    else:
        print_error(message)

    # Summary
    print_section("VERIFICATION SUMMARY")
    all_passed = True
    for check, passed in results.items():
        if passed:
            print_success(f"{check:30s} - PASSED")
        else:
            print_error(f"{check:30s} - FAILED")
            all_passed = False

    # Final status
    print("\n" + "=" * 70)
    if all_passed:
        print_success(
            f"\n{Colors.BOLD}🎉 All checks passed! Project is ready to use!{Colors.RESET}\n"
        )
        print("Next steps:")
        print("  1. Train models:        python src/training/train.py")
        print("  2. Register model:      python scripts/register_model.py")
        print("  3. Start API:           python src/api/main.py")
        print("  4. Or use Docker:       docker-compose up -d")
        print("  5. View MLflow UI:      mlflow ui")
    else:
        print_error(
            f"\n{Colors.BOLD}⚠️  Some checks failed. Please fix the issues above.{Colors.RESET}\n"
        )
        print("Common fixes:")
        print("  • Install packages:     pip install -r requirements.txt")
        print("  • Install dev tools:    pip install -r requirements-dev.txt")
        print("  • Create .env:          cp .env.example .env")
        print("  • Run setup script:     ./setup.sh")

    print("=" * 70 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
