# ML Training Pipeline Documentation

> **Technical documentation for the MNIST classification ML pipeline**

---

## Table of Contents
1. [Overview](#overview)
2. [Dataset](#dataset)
3. [Model Architecture](#model-architecture)
4. [Training Strategy](#training-strategy)
5. [Experiment Tracking](#experiment-tracking)
6. [Model Evaluation](#model-evaluation)
7. [Best Practices](#best-practices)

---

## Overview

The MNIST ML pipeline implements a systematic approach to model development through controlled experimentation. The pipeline demonstrates enterprise MLOps practices including experiment tracking, model versioning, and reproducibility.

**Key Features:**
- Three progressive experiment runs (Baseline → Enhanced → Optimized)
- Comprehensive MLflow experiment tracking
- Automated model registration
- Reproducible training pipeline
- Systematic hyperparameter tuning

---

## Dataset

### MNIST Dataset Characteristics

**Source**: MNIST Handwritten Digits Database
**Provider**: Yann LeCun, Corinna Cortes, Christopher J.C. Burges

**Statistics:**
- **Training Set**: 60,000 grayscale images
- **Test Set**: 10,000 grayscale images
- **Image Dimensions**: 28×28 pixels
- **Classes**: 10 (digits 0-9)
- **Format**: Grayscale, normalized to [0, 1]

### Data Preprocessing Pipeline

```python
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

# 1. Load Dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 2. Normalization
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# 3. Reshaping for CNN
x_train = x_train.reshape(-1, 28, 28, 1)  # Add channel dimension
x_test = x_test.reshape(-1, 28, 28, 1)

# 4. One-Hot Encoding Labels
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)
```

**Preprocessing Steps:**
1. **Normalization**: Scale pixel values from [0, 255] to [0, 1]
2. **Reshaping**: Add channel dimension for CNN (28, 28) → (28, 28, 1)
3. **Label Encoding**: Convert labels to one-hot vectors (10 classes)

---

## Model Architecture

### Run 1: Baseline Model

**Purpose**: Establish performance baseline with minimal architecture

```python
def build_baseline_model():
    model = Sequential([
        Conv2D(32, kernel_size=(3, 3), activation='relu',
               input_shape=(28, 28, 1)),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(10, activation='softmax')
    ])
    return model
```

**Architecture Details:**
- **Conv2D Layer**: 32 filters, 3×3 kernel, ReLU activation
  - Input: (28, 28, 1)
  - Output: (26, 26, 32)
- **MaxPooling2D**: 2×2 pool size
  - Output: (13, 13, 32)
- **Flatten**: Convert to 1D vector
  - Output: 5,408 features
- **Dense Output**: 10 units, softmax activation
  - Output: 10 class probabilities

**Parameters**: ~5,450
**Expected Accuracy**: ~98.0%

**Rationale**: Simple architecture to establish baseline. Minimal layers to verify training pipeline works correctly.

---

### Run 2: Enhanced Model

**Purpose**: Improve generalization with regularization and increased capacity

```python
def build_enhanced_model():
    model = Sequential([
        Conv2D(64, kernel_size=(3, 3), activation='relu',
               input_shape=(28, 28, 1)),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(10, activation='softmax')
    ])
    return model
```

**Architecture Details:**
- **Conv2D Layer**: 64 filters, 3×3 kernel, ReLU activation
  - Doubled filters for increased capacity
  - Output: (26, 26, 64)
- **MaxPooling2D**: 2×2 pool size
  - Output: (13, 13, 64)
- **Dropout(0.25)**: Drop 25% of features
  - Prevents overfitting in convolutional layers
- **Flatten**: Convert to 1D vector
  - Output: 10,816 features
- **Dense Hidden**: 128 units, ReLU activation
  - Learns complex feature combinations
- **Dropout(0.5)**: Drop 50% of neurons
  - Strong regularization before output
- **Dense Output**: 10 units, softmax activation

**Parameters**: ~1,395,978
**Expected Accuracy**: ~98.5%

**Improvements over Run 1:**
- ✅ Dropout layers prevent overfitting
- ✅ Doubled filters capture more complex patterns
- ✅ Hidden dense layer learns higher-level features
- ✅ Better generalization to unseen data

---

### Run 3: Optimized Model

**Purpose**: Fine-tune hyperparameters for optimal performance

```python
def build_optimized_model():
    # Same architecture as Run 2
    model = build_enhanced_model()
    return model
```

**Architecture**: Identical to Run 2
**Change**: Hyperparameter optimization (not architecture)

**Hyperparameter Changes:**
- **Learning Rate**: 0.001 → 0.0005 (50% reduction)
  - Slower, more precise convergence
  - Avoids overshooting optimal weights
- **Batch Size**: 128 → 64 (50% reduction)
  - More frequent weight updates
  - Better gradient estimates
  - Improved generalization

**Expected Accuracy**: ~99.0%+

**Rationale**: Smaller learning rate and batch size allow model to find better local minima. This is more computationally expensive but yields better final performance.

---

## Training Strategy

### Training Configuration

**Common Settings (All Runs):**
```python
EPOCHS = 5
OPTIMIZER = Adam()
LOSS = 'categorical_crossentropy'
METRICS = ['accuracy']
VALIDATION_SPLIT = 0.1  # 10% of training data
```

### Hyperparameter Matrix

| Parameter | Run 1 (Baseline) | Run 2 (Enhanced) | Run 3 (Optimized) |
|-----------|------------------|------------------|-------------------|
| **Filters** | 32 | 64 | 64 |
| **Hidden Units** | 0 | 128 | 128 |
| **Dropout** | None | 0.25, 0.5 | 0.25, 0.5 |
| **Learning Rate** | 0.001 | 0.001 | 0.0005 |
| **Batch Size** | 128 | 128 | 64 |
| **Epochs** | 5 | 5 | 5 |
| **Optimizer** | Adam | Adam | Adam |

### Training Execution

```python
# Run training with MLflow tracking
with mlflow.start_run(run_name=run_name):
    # Log hyperparameters
    mlflow.log_params({
        "model_type": model_type,
        "learning_rate": learning_rate,
        "batch_size": batch_size,
        "epochs": epochs
    })

    # Train model
    history = model.fit(
        x_train, y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_split=0.1,
        verbose=1
    )

    # Log metrics per epoch
    for epoch in range(epochs):
        mlflow.log_metrics({
            "train_loss": history.history['loss'][epoch],
            "train_accuracy": history.history['accuracy'][epoch],
            "val_loss": history.history['val_loss'][epoch],
            "val_accuracy": history.history['val_accuracy'][epoch]
        }, step=epoch)

    # Evaluate on test set
    test_loss, test_accuracy = model.evaluate(x_test, y_test)
    mlflow.log_metrics({
        "test_loss": test_loss,
        "test_accuracy": test_accuracy
    })

    # Save model
    mlflow.tensorflow.log_model(model, "model")
```

---

## Experiment Tracking

### MLflow Integration

**Tracking Components:**
1. **Parameters**: Model architecture, hyperparameters
2. **Metrics**: Training/validation/test accuracy and loss
3. **Artifacts**: Model files, training curves, confusion matrix
4. **Tags**: Run metadata, experiment type

### Logged Metrics

**Per-Epoch Metrics:**
- `train_loss`: Training loss (categorical cross-entropy)
- `train_accuracy`: Training accuracy (%)
- `val_loss`: Validation loss
- `val_accuracy`: Validation accuracy (%)

**Final Metrics:**
- `test_loss`: Test set loss
- `test_accuracy`: Test set accuracy (%)

### Experiment Comparison

**View in MLflow UI:**
```bash
mlflow ui --port 5000
# Open http://localhost:5000
```

**Compare Runs:**
1. Select all 3 runs
2. Click "Compare"
3. View parallel coordinates plot
4. Analyze metric trends

---

## Model Evaluation

### Evaluation Metrics

**Primary Metric**: Test Accuracy
- Measures overall classification performance
- Target: >99% for production deployment

**Secondary Metrics**:
- **Loss**: Cross-entropy loss (lower is better)
- **Confusion Matrix**: Per-class accuracy analysis
- **Training Time**: Computational efficiency

### Expected Results

| Run | Test Accuracy | Test Loss | Training Time |
|-----|---------------|-----------|---------------|
| Run 1 | ~98.0% | ~0.06 | ~2 min |
| Run 2 | ~98.5% | ~0.05 | ~3 min |
| Run 3 | ~99.0%+ | ~0.04 | ~4 min |

### Model Selection Criteria

**Best Model Selection:**
1. Highest test accuracy
2. Lowest validation loss
3. Minimal overfitting (train vs. validation gap)
4. Reasonable training time

**Production Criteria:**
- Test accuracy ≥ 99%
- Inference latency < 100ms
- Model size < 10MB
- No significant bias across classes

---

## Best Practices

### Reproducibility

**Ensure reproducibility:**
```python
import random
import numpy as np
import tensorflow as tf

# Set seeds
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)
```

**MLflow tracking:**
- Log all hyperparameters
- Log git commit hash
- Log dependency versions
- Store complete model artifacts

### Experiment Design

**Progressive Refinement:**
1. **Baseline**: Simple model, verify pipeline
2. **Architecture**: Improve model capacity
3. **Hyperparameters**: Optimize training process
4. **Ensemble** (optional): Combine best models

**Controlled Variables:**
- Change one aspect at a time
- Keep epochs constant for fair comparison
- Use same train/test split
- Document all changes

### Monitoring Training

**Watch for:**
- **Overfitting**: Train accuracy >> Validation accuracy
- **Underfitting**: Both accuracies plateau at low values
- **Unstable training**: Loss oscillates or increases
- **Slow convergence**: Accuracy improves very slowly

**Solutions:**
- **Overfitting**: Add dropout, reduce model size, use data augmentation
- **Underfitting**: Increase model capacity, train longer
- **Instability**: Reduce learning rate, use gradient clipping
- **Slow convergence**: Increase learning rate, use batch normalization

### Model Debugging

**If accuracy is low:**
1. Check data preprocessing (normalization, reshaping)
2. Verify labels are correctly encoded
3. Try simpler architecture first
4. Reduce learning rate
5. Check for data leakage

**If training is slow:**
1. Reduce batch size (uses less memory)
2. Reduce model complexity
3. Use GPU acceleration
4. Profile code for bottlenecks

---

## Code Examples

### Complete Training Script

```python
import mlflow
from src.data.loader import load_mnist_data
from src.models.cnn import build_baseline_model
from src.utils.config import Config

# Load configuration
config = Config()
mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
mlflow.set_experiment(config.EXPERIMENT_NAME)

# Load data
(x_train, y_train), (x_test, y_test) = load_mnist_data()

# Run 1: Baseline
with mlflow.start_run(run_name="run_1_baseline"):
    model = build_baseline_model()
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    mlflow.log_params({
        "model_type": "baseline",
        "filters": 32,
        "learning_rate": 0.001,
        "batch_size": 128,
        "epochs": 5
    })

    history = model.fit(
        x_train, y_train,
        batch_size=128,
        epochs=5,
        validation_split=0.1
    )

    test_loss, test_accuracy = model.evaluate(x_test, y_test)
    mlflow.log_metrics({
        "test_loss": test_loss,
        "test_accuracy": test_accuracy
    })

    mlflow.tensorflow.log_model(model, "model")
```

### Model Registration

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Find best run
experiment = client.get_experiment_by_name("MNIST_Classification")
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.test_accuracy DESC"],
    max_results=1
)

best_run = runs[0]

# Register model
model_uri = f"runs:/{best_run.info.run_id}/model"
mlflow.register_model(
    model_uri=model_uri,
    name="Mnist_Best_Model",
    tags={"stage": "production"}
)

# Transition to production
client.transition_model_version_stage(
    name="Mnist_Best_Model",
    version=1,
    stage="Production"
)
```

---

## Performance Benchmarks

### Hardware Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 4GB
- Storage: 2GB

**Recommended:**
- CPU: 4+ cores or GPU
- RAM: 8GB+
- Storage: 10GB

### Training Performance

**CPU (Intel i5):**
- Run 1: ~2 minutes
- Run 2: ~3 minutes
- Run 3: ~4 minutes
- Total: ~10 minutes

**GPU (NVIDIA GTX 1060):**
- Run 1: ~30 seconds
- Run 2: ~45 seconds
- Run 3: ~60 seconds
- Total: ~2.5 minutes

### Inference Performance

**Single Prediction:**
- Model loading: ~1-2 seconds (one-time)
- Preprocessing: <1ms
- Inference: ~5-10ms (CPU)
- Total latency: ~10-15ms

**Batch Prediction (32 images):**
- Preprocessing: ~5ms
- Inference: ~20-30ms
- Per-image: ~1ms

---

## Troubleshooting

### Common Issues

**Issue**: Model accuracy stuck at ~10%
- **Cause**: Model predicting same class for all inputs
- **Solution**: Check label encoding, verify one-hot conversion

**Issue**: Validation accuracy much lower than training
- **Cause**: Overfitting
- **Solution**: Add dropout, reduce model size, use data augmentation

**Issue**: Training very slow
- **Cause**: Large batch size or CPU bottleneck
- **Solution**: Reduce batch size, use GPU, enable mixed precision

**Issue**: MLflow run not appearing
- **Cause**: Tracking URI not set or mlflow server not running
- **Solution**: Set `MLFLOW_TRACKING_URI`, start mlflow ui

---

**Document Version**: 1.0
**Last Updated**: December 2025
**For More Info**: See [ARCHITECTURE.md](ARCHITECTURE.md) for system architecture
