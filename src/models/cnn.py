"""CNN model architectures for MNIST classification."""

from typing import List

from tensorflow import keras
from tensorflow.keras import layers

from src.utils.logger import get_logger

logger = get_logger(__name__)


def create_baseline_model(input_shape: tuple = (28, 28, 1), num_classes: int = 10) -> keras.Model:
    """
    Create baseline CNN model (Run 1).

    Simple architecture with 1 Conv2D layer and 1 Dense layer.
    Purpose: Establish baseline performance.

    Args:
        input_shape: Shape of input images (height, width, channels).
        num_classes: Number of output classes.

    Returns:
        Compiled Keras model.
    """
    logger.info("Creating baseline CNN model...")

    model = keras.Sequential(
        [
            layers.Input(shape=input_shape),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu", name="conv1"),
            layers.MaxPooling2D(pool_size=(2, 2), name="pool1"),
            layers.Flatten(name="flatten"),
            layers.Dense(num_classes, activation="softmax", name="output"),
        ],
        name="baseline_model",
    )

    logger.info(f"Model created: {model.name}")
    return model


def create_improved_architecture_model(
    input_shape: tuple = (28, 28, 1), num_classes: int = 10
) -> keras.Model:
    """
    Create improved architecture CNN model (Run 2).

    Added Dropout layers and increased filters to prevent overfitting.
    Purpose: Verify if more complex model learns better.

    Args:
        input_shape: Shape of input images (height, width, channels).
        num_classes: Number of output classes.

    Returns:
        Compiled Keras model.
    """
    logger.info("Creating improved architecture CNN model...")

    model = keras.Sequential(
        [
            layers.Input(shape=input_shape),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu", name="conv1"),
            layers.MaxPooling2D(pool_size=(2, 2), name="pool1"),
            layers.Dropout(0.25, name="dropout1"),
            layers.Flatten(name="flatten"),
            layers.Dense(128, activation="relu", name="dense1"),
            layers.Dropout(0.5, name="dropout2"),
            layers.Dense(num_classes, activation="softmax", name="output"),
        ],
        name="improved_model",
    )

    logger.info(f"Model created: {model.name}")
    return model


def create_optimized_model(input_shape: tuple = (28, 28, 1), num_classes: int = 10) -> keras.Model:
    """
    Create optimized CNN model (Run 3).

    Same architecture as Run 2, but will use different hyperparameters.
    Purpose: Optimize model convergence speed.

    Args:
        input_shape: Shape of input images (height, width, channels).
        num_classes: Number of output classes.

    Returns:
        Compiled Keras model.
    """
    logger.info("Creating optimized CNN model...")

    model = keras.Sequential(
        [
            layers.Input(shape=input_shape),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu", name="conv1"),
            layers.MaxPooling2D(pool_size=(2, 2), name="pool1"),
            layers.Dropout(0.25, name="dropout1"),
            layers.Flatten(name="flatten"),
            layers.Dense(128, activation="relu", name="dense1"),
            layers.Dropout(0.5, name="dropout2"),
            layers.Dense(num_classes, activation="softmax", name="output"),
        ],
        name="optimized_model",
    )

    logger.info(f"Model created: {model.name}")
    return model


def get_model_config(model_type: str) -> dict:
    """
    Get hyperparameter configuration for different model types.

    Args:
        model_type: Type of model ("baseline", "improved", "optimized").

    Returns:
        Dictionary containing hyperparameter configuration.

    Raises:
        ValueError: If model_type is invalid.
    """
    configs = {
        "baseline": {
            "learning_rate": 0.001,
            "batch_size": 128,
            "epochs": 5,
            "optimizer": "adam",
        },
        "improved": {
            "learning_rate": 0.001,
            "batch_size": 128,
            "epochs": 5,
            "optimizer": "adam",
        },
        "optimized": {
            "learning_rate": 0.0005,
            "batch_size": 64,
            "epochs": 5,
            "optimizer": "adam",
        },
    }

    if model_type not in configs:
        raise ValueError(f"Invalid model_type: {model_type}. Must be one of {list(configs.keys())}")

    return configs[model_type]
