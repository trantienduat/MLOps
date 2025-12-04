"""
MNIST Training Script with MLflow Experiment Tracking

This script trains three different CNN models on MNIST dataset:
- Run 1 (Baseline): Basic CNN with 1 Conv2D layer
- Run 2 (Tuning Architecture): Added Dropout and increased filters
- Run 3 (Tuning Hyperparameters): Modified learning rate and batch size
"""

import mlflow
import mlflow.tensorflow
import tensorflow as tf
try:
    from tensorflow import keras
    from tensorflow.keras import layers
except ImportError:
    # Fallback for older TensorFlow versions
    import keras
    from keras import layers
import numpy as np
import matplotlib.pyplot as plt

[...full content from original train.py...]
