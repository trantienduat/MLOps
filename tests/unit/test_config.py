"""Unit tests for configuration module."""
import os

import pytest

from src.utils.config import Config


class TestConfig:
    """Test cases for Config class."""

    def test_default_values(self):
        """Test that default configuration values are set correctly."""
        assert Config.MODEL_NAME == "Mnist_Best_Model"
        assert Config.EXPERIMENT_NAME == "MNIST_Classification_Experiments"
        assert Config.MODEL_STAGE == "Production"

    def test_mlflow_uri_default(self):
        """Test default MLflow tracking URI."""
        uri = Config.get_mlflow_uri()
        assert uri == "http://localhost:5000"

    def test_environment_checks(self):
        """Test environment checking methods."""
        # In test environment, default should be development
        assert Config.is_development()
        assert not Config.is_production()

    def test_api_configuration(self):
        """Test API configuration values."""
        assert Config.API_HOST == "0.0.0.0"
        assert Config.API_PORT == 8000
        assert Config.API_WORKERS >= 1

    def test_validate_invalid_port_raises_error(self):
        """Test that invalid port raises error during validation."""
        original_port = Config.API_PORT
        try:
            Config.API_PORT = 99999
            with pytest.raises(ValueError, match="Invalid API_PORT"):
                Config.validate()
        finally:
            Config.API_PORT = original_port

    def test_validate_invalid_workers_raises_error(self):
        """Test that invalid workers count raises error."""
        original_workers = Config.API_WORKERS
        try:
            Config.API_WORKERS = 0
            with pytest.raises(ValueError, match="Invalid API_WORKERS"):
                Config.validate()
        finally:
            Config.API_WORKERS = original_workers

    def test_production_secret_key_validation(self):
        """Test that production environment requires proper secret key."""
        original_env = Config.ENVIRONMENT
        original_key = Config.SECRET_KEY

        try:
            Config.ENVIRONMENT = "production"
            Config.SECRET_KEY = "dev-secret-key-change-in-production"

            with pytest.raises(ValueError, match="SECRET_KEY must be set in production"):
                Config.validate()
        finally:
            Config.ENVIRONMENT = original_env
            Config.SECRET_KEY = original_key
