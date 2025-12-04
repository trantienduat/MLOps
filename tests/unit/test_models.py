"""Unit tests for CNN models."""
import pytest
from tensorflow import keras

from src.models.cnn import (
    create_baseline_model,
    create_improved_architecture_model,
    create_optimized_model,
    get_model_config,
)


class TestModelCreation:
    """Test cases for model creation functions."""

    def test_baseline_model_creation(self):
        """Test that baseline model is created with correct architecture."""
        model = create_baseline_model()

        assert isinstance(model, keras.Model)
        assert model.name == "baseline_model"
        assert len(model.layers) == 5  # Input, Conv2D, MaxPool, Flatten, Dense

    def test_improved_model_creation(self):
        """Test that improved model is created with dropout layers."""
        model = create_improved_architecture_model()

        assert isinstance(model, keras.Model)
        assert model.name == "improved_model"
        assert any("dropout" in layer.name for layer in model.layers)

    def test_optimized_model_creation(self):
        """Test that optimized model is created successfully."""
        model = create_optimized_model()

        assert isinstance(model, keras.Model)
        assert model.name == "optimized_model"

    def test_models_have_correct_output_shape(self):
        """Test that all models have correct output shape."""
        models = [
            create_baseline_model(),
            create_improved_architecture_model(),
            create_optimized_model(),
        ]

        for model in models:
            assert model.output_shape == (None, 10)

    def test_custom_input_shape(self):
        """Test models can be created with custom input shape."""
        model = create_baseline_model(input_shape=(32, 32, 3), num_classes=5)

        assert model.output_shape == (None, 5)


class TestModelConfig:
    """Test cases for model configuration."""

    def test_baseline_config(self):
        """Test baseline model configuration."""
        config = get_model_config("baseline")

        assert config["learning_rate"] == 0.001
        assert config["batch_size"] == 128
        assert config["epochs"] == 5

    def test_improved_config(self):
        """Test improved model configuration."""
        config = get_model_config("improved")

        assert "learning_rate" in config
        assert "batch_size" in config
        assert "epochs" in config

    def test_optimized_config(self):
        """Test optimized model configuration."""
        config = get_model_config("optimized")

        assert config["learning_rate"] == 0.0005
        assert config["batch_size"] == 64

    def test_invalid_model_type_raises_error(self):
        """Test that invalid model type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid model_type"):
            get_model_config("invalid_type")
