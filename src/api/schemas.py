"""Pydantic schemas for API request/response validation."""
from typing import List

from pydantic import BaseModel, Field, field_validator


class PredictionRequest(BaseModel):
    """Request schema for image prediction."""

    image: str = Field(..., description="Base64 encoded image data")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            }
        }


class PredictionResponse(BaseModel):
    """Response schema for prediction results."""

    prediction: int = Field(..., description="Predicted class (0-9)", ge=0, le=9)
    confidence: float = Field(..., description="Confidence score", ge=0.0, le=1.0)
    probabilities: List[float] = Field(..., description="Probability distribution over all classes")

    @field_validator("probabilities")
    @classmethod
    def validate_probabilities_length(cls, v: List[float]) -> List[float]:
        """Validate that probabilities list has 10 elements."""
        if len(v) != 10:
            raise ValueError("Probabilities must have exactly 10 elements")
        return v

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "prediction": 5,
                "confidence": 0.9876,
                "probabilities": [0.001, 0.002, 0.003, 0.001, 0.002, 0.9876, 0.001, 0.001, 0.001, 0.001],
            }
        }


class HealthResponse(BaseModel):
    """Response schema for health check."""

    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    model_name: str = Field(..., description="Name of loaded model")
    model_version: str = Field(..., description="Version of loaded model")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "model_name": "Mnist_Best_Model",
                "model_version": "1",
            }
        }


class ErrorResponse(BaseModel):
    """Response schema for errors."""

    detail: str = Field(..., description="Error details")
    error_type: str = Field(..., description="Type of error")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {"example": {"detail": "Invalid image format", "error_type": "ValidationError"}}
