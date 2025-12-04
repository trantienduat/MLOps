"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

import pytest

# Add src directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_dir():
    """Return project root directory."""
    return project_root


@pytest.fixture(scope="session")
def src_dir(project_root_dir):
    """Return src directory."""
    return project_root_dir / "src"


# Configure pytest markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
