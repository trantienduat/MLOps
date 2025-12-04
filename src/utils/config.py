"""Utility module for centralized configuration management."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class with environment-based settings."""

    # MLflow Configuration
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "Mnist_Best_Model")
    EXPERIMENT_NAME: str = os.getenv("EXPERIMENT_NAME", "MNIST_Classification_Experiments")
    MODEL_STAGE: str = os.getenv("MODEL_STAGE", "Production")

    # Application Configuration
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_WORKERS: int = int(os.getenv("API_WORKERS", "4"))

    # Model Configuration
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    API_KEY: Optional[str] = os.getenv("API_KEY")

    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    SRC_DIR: Path = PROJECT_ROOT / "src"
    MLRUNS_DIR: Path = PROJECT_ROOT / "mlruns"

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return cls.ENVIRONMENT.lower() == "production"

    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment."""
        return cls.ENVIRONMENT.lower() == "development"

    @classmethod
    def get_mlflow_uri(cls) -> str:
        """Get MLflow tracking URI."""
        return cls.MLFLOW_TRACKING_URI

    @classmethod
    def validate(cls) -> None:
        """Validate configuration settings."""
        if cls.is_production() and cls.SECRET_KEY == "dev-secret-key-change-in-production":
            raise ValueError("SECRET_KEY must be set in production environment")

        if cls.API_PORT < 1 or cls.API_PORT > 65535:
            raise ValueError(f"Invalid API_PORT: {cls.API_PORT}")

        if cls.API_WORKERS < 1:
            raise ValueError(f"Invalid API_WORKERS: {cls.API_WORKERS}")


# Create a singleton instance
config = Config()
