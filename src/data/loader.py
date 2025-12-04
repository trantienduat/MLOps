"""Data loading and preprocessing utilities for MNIST dataset."""

from typing import Tuple

import numpy as np
import numpy.typing as npt
from tensorflow import keras

from src.utils.logger import get_logger

logger = get_logger(__name__)


def load_mnist_data() -> Tuple[
    Tuple[npt.NDArray[np.float32], npt.NDArray[np.int64]],
    Tuple[npt.NDArray[np.float32], npt.NDArray[np.int64]],
]:
    """
    Load and preprocess MNIST dataset.

    Returns:
        Tuple containing:
            - Training data: (x_train, y_train)
            - Test data: (x_test, y_test)

    Raises:
        RuntimeError: If dataset cannot be loaded.
    """
    try:
        logger.info("Loading MNIST dataset...")
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

        # Normalize pixel values to [0, 1]
        x_train = x_train.astype("float32") / 255.0
        x_test = x_test.astype("float32") / 255.0

        # Reshape to add channel dimension (28, 28, 1)
        x_train = np.expand_dims(x_train, -1)
        x_test = np.expand_dims(x_test, -1)

        logger.info(f"Training data shape: {x_train.shape}")
        logger.info(f"Test data shape: {x_test.shape}")
        logger.info(f"Number of classes: {len(np.unique(y_train))}")

        return (x_train, y_train), (x_test, y_test)

    except Exception as e:
        logger.error(f"Failed to load MNIST dataset: {e}")
        raise RuntimeError(f"Dataset loading failed: {e}") from e


def preprocess_image(image: npt.NDArray[np.uint8]) -> npt.NDArray[np.float32]:
    """
    Preprocess a single image for model prediction.

    Args:
        image: Input image array of shape (28, 28) or (28, 28, 1).

    Returns:
        Preprocessed image array of shape (1, 28, 28, 1).

    Raises:
        ValueError: If image shape is invalid.
    """
    if image.shape not in [(28, 28), (28, 28, 1)]:
        raise ValueError(f"Invalid image shape: {image.shape}. Expected (28, 28) or (28, 28, 1)")

    # Normalize
    image = image.astype("float32") / 255.0

    # Ensure correct shape
    if len(image.shape) == 2:
        image = np.expand_dims(image, -1)

    # Add batch dimension
    image = np.expand_dims(image, 0)

    return image
