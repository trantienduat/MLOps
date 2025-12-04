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


def load_mnist_data():
    """Load and preprocess MNIST dataset."""
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    
    # Normalize pixel values to [0, 1]
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    # Reshape to add channel dimension (28, 28, 1)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    
    print(f"Training data shape: {x_train.shape}")
    print(f"Test data shape: {x_test.shape}")
    
    return (x_train, y_train), (x_test, y_test)


def create_baseline_model():
    """
    Run 1: Baseline CNN model
    - Simple architecture: 1 Conv2D layer, 1 Dense layer
    - Purpose: Establish baseline performance
    """
    model = keras.Sequential([
        layers.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(10, activation='softmax')
    ])
    return model


def create_improved_architecture_model():
    """
    Run 2: Improved architecture
    - Added Dropout layer to prevent overfitting
    - Increased number of filters
    - Purpose: Verify if more complex model learns better
    """
    model = keras.Sequential([
        layers.Input(shape=(28, 28, 1)),
        layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.25),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])
    return model


def create_optimized_model():
    """
    Run 3: Same architecture as Run 2
    - Will use different hyperparameters (learning rate, batch size)
    - Purpose: Optimize model convergence speed
    """
    model = keras.Sequential([
        layers.Input(shape=(28, 28, 1)),
        layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.25),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])
    return model


def train_model(model, x_train, y_train, x_test, y_test, 
                learning_rate=0.001, batch_size=128, epochs=5, run_name=""):
    """
    Train model with MLflow tracking.
    
    Args:
        model: Keras model to train
        x_train, y_train: Training data
        x_test, y_test: Test data
        learning_rate: Learning rate for optimizer
        batch_size: Batch size for training
        epochs: Number of training epochs
        run_name: Name for this MLflow run
    """
    with mlflow.start_run(run_name=run_name):
        # Log parameters
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("optimizer", "adam")
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Log model summary
        model_summary = []
        model.summary(print_fn=lambda x: model_summary.append(x))
        mlflow.log_text('\n'.join(model_summary), "model_summary.txt")
        
        # Train model
        history = model.fit(
            x_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_split=0.1,
            verbose=1
        )
        
        # Evaluate on test set
        test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
        
        # Log metrics
        mlflow.log_metric("test_loss", test_loss)
        mlflow.log_metric("test_accuracy", test_accuracy)
        
        # Log training history
        for epoch in range(epochs):
            mlflow.log_metric("train_loss", history.history['loss'][epoch], step=epoch)
            mlflow.log_metric("train_accuracy", history.history['accuracy'][epoch], step=epoch)
            mlflow.log_metric("val_loss", history.history['val_loss'][epoch], step=epoch)
            mlflow.log_metric("val_accuracy", history.history['val_accuracy'][epoch], step=epoch)
        
        # Create and log training curves
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Plot loss
        ax1.plot(history.history['loss'], label='Train Loss')
        ax1.plot(history.history['val_loss'], label='Val Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.set_title('Model Loss')
        ax1.legend()
        ax1.grid(True)
        
        # Plot accuracy
        ax2.plot(history.history['accuracy'], label='Train Accuracy')
        ax2.plot(history.history['val_accuracy'], label='Val Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy')
        ax2.set_title('Model Accuracy')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        mlflow.log_figure(fig, "training_curves.png")
        plt.close()
        
        # Log model
        mlflow.tensorflow.log_model(model, "model")
        
        print(f"\n{run_name} - Test Accuracy: {test_accuracy:.4f}, Test Loss: {test_loss:.4f}")
        
        return model, history


def main():
    """Main execution function to run all three experiments."""
    print("=" * 60)
    print("MNIST MLOps Training Pipeline")
    print("=" * 60)
    
    # Set MLflow experiment name
    mlflow.set_experiment("MNIST_Classification_Experiments")
    
    # Load data
    print("\nLoading MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = load_mnist_data()
    
    # Run 1: Baseline
    print("\n" + "=" * 60)
    print("RUN 1: BASELINE MODEL")
    print("Purpose: Establish baseline performance")
    print("=" * 60)
    model_baseline = create_baseline_model()
    train_model(
        model_baseline, x_train, y_train, x_test, y_test,
        learning_rate=0.001,
        batch_size=128,
        epochs=5,
        run_name="Run_1_Baseline"
    )
    
    # Run 2: Improved Architecture
    print("\n" + "=" * 60)
    print("RUN 2: IMPROVED ARCHITECTURE")
    print("Purpose: Add Dropout and increase filters to improve learning")
    print("=" * 60)
    model_improved = create_improved_architecture_model()
    train_model(
        model_improved, x_train, y_train, x_test, y_test,
        learning_rate=0.001,
        batch_size=128,
        epochs=5,
        run_name="Run_2_Improved_Architecture"
    )
    
    # Run 3: Hyperparameter Tuning
    print("\n" + "=" * 60)
    print("RUN 3: HYPERPARAMETER TUNING")
    print("Purpose: Optimize convergence with adjusted learning rate and batch size")
    print("=" * 60)
    model_optimized = create_optimized_model()
    train_model(
        model_optimized, x_train, y_train, x_test, y_test,
        learning_rate=0.0005,  # Reduced learning rate
        batch_size=64,         # Smaller batch size
        epochs=5,
        run_name="Run_3_Hyperparameter_Tuning"
    )
    
    print("\n" + "=" * 60)
    print("All experiments completed!")
    print("View results at: http://127.0.0.1:5000")
    print("Run command: mlflow ui")
    print("=" * 60)


if __name__ == "__main__":
    main()
