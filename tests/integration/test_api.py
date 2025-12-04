"""Integration tests for the FastAPI application."""

import base64
import io

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

# Note: In real scenario, mock the model loading
# from unittest.mock import MagicMock, patch


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    # This will need to be updated to properly mock model loading
    # For now, this is a template
    from src.api.main import app

    return TestClient(app)


@pytest.fixture
def sample_image_base64():
    """Create a sample base64 encoded image."""
    # Create a simple 28x28 image
    image = Image.new("L", (28, 28), color=128)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()
    return base64.b64encode(image_bytes).decode("utf-8")


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert "model_loaded" in data
    assert "model_name" in data


def test_api_info_endpoint(client):
    """Test API info endpoint."""
    response = client.get("/api/info")
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "MNIST Classification API"
    assert "version" in data
    assert "model_name" in data


# Note: These tests will need proper mocking to work without a real model
# def test_predict_endpoint(client, sample_image_base64):
#     """Test prediction endpoint with valid image."""
#     response = client.post(
#         "/predict",
#         json={"image": f"data:image/png;base64,{sample_image_base64}"}
#     )
#
#     # This will fail without model loaded
#     # In production tests, mock the model
#     assert response.status_code in [200, 503]


def test_predict_endpoint_invalid_format(client):
    """Test prediction endpoint with invalid image format."""
    response = client.post("/predict", json={"image": "invalid_base64"})

    # Should return error
    assert response.status_code in [422, 500]


def test_metrics_endpoint_exists(client):
    """Test that Prometheus metrics endpoint exists."""
    response = client.get("/metrics")
    assert response.status_code == 200
