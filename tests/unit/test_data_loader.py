"""Unit tests for data loader module."""
import numpy as np
import pytest

from src.data.loader import load_mnist_data, preprocess_image


class TestLoadMnistData:
    """Test cases for load_mnist_data function."""

    def test_load_mnist_returns_correct_shapes(self):
        """Test that MNIST data is loaded with correct shapes."""
        (x_train, y_train), (x_test, y_test) = load_mnist_data()

        assert x_train.shape == (60000, 28, 28, 1)
        assert x_test.shape == (10000, 28, 28, 1)
        assert y_train.shape == (60000,)
        assert y_test.shape == (10000,)

    def test_load_mnist_normalizes_values(self):
        """Test that pixel values are normalized to [0, 1]."""
        (x_train, y_train), (x_test, y_test) = load_mnist_data()

        assert x_train.min() >= 0.0
        assert x_train.max() <= 1.0
        assert x_test.min() >= 0.0
        assert x_test.max() <= 1.0

    def test_load_mnist_has_10_classes(self):
        """Test that dataset contains 10 digit classes."""
        (x_train, y_train), (x_test, y_test) = load_mnist_data()

        unique_classes = np.unique(y_train)
        assert len(unique_classes) == 10
        assert all(0 <= c <= 9 for c in unique_classes)


class TestPreprocessImage:
    """Test cases for preprocess_image function."""

    def test_preprocess_2d_image(self):
        """Test preprocessing of 2D image array."""
        image = np.random.randint(0, 256, (28, 28), dtype=np.uint8)
        processed = preprocess_image(image)

        assert processed.shape == (1, 28, 28, 1)
        assert processed.min() >= 0.0
        assert processed.max() <= 1.0

    def test_preprocess_3d_image(self):
        """Test preprocessing of 3D image array."""
        image = np.random.randint(0, 256, (28, 28, 1), dtype=np.uint8)
        processed = preprocess_image(image)

        assert processed.shape == (1, 28, 28, 1)

    def test_preprocess_invalid_shape_raises_error(self):
        """Test that invalid image shape raises ValueError."""
        image = np.random.randint(0, 256, (32, 32), dtype=np.uint8)

        with pytest.raises(ValueError, match="Invalid image shape"):
            preprocess_image(image)

    def test_preprocess_normalizes_values(self):
        """Test that preprocessing normalizes pixel values."""
        image = np.full((28, 28), 255, dtype=np.uint8)
        processed = preprocess_image(image)

        assert np.allclose(processed, 1.0)
