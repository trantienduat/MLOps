"""
Flask Web Application for MNIST Digit Recognition

This application allows users to draw digits on a canvas and get predictions
from a trained MLflow model.
"""

from flask import Flask, render_template, request, jsonify
import mlflow
import mlflow.tensorflow
import numpy as np
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

# Global variable to store the loaded model
model = None


def load_model():
    """
    Load the best model from MLflow Model Registry.
    
    Returns:
        Loaded Keras model
    """
    global model
    
    try:
        # Option 1: Load from MLflow Model Registry (Production stage)
        model_name = "Mnist_Best_Model"
        model_uri = f"models:/{model_name}/Production"
        
        print(f"Attempting to load model from registry: {model_uri}")
        model = mlflow.tensorflow.load_model(model_uri)
        print("Successfully loaded model from Model Registry (Production)")
        return model
        
    except Exception as e:
        print(f"Could not load from Model Registry: {e}")
        
        try:
            # Option 2: Load from latest run in MLflow
            # Find the latest run with the best accuracy
            client = mlflow.MlflowClient()
            experiment = client.get_experiment_by_name("MNIST_Classification_Experiments")
            
            if experiment:
                runs = client.search_runs(
                    experiment_ids=[experiment.experiment_id],
                    order_by=["metrics.test_accuracy DESC"],
                    max_results=1
                )
                
                if runs:
                    best_run = runs[0]
                    model_uri = f"runs:/{best_run.info.run_id}/model"
                    print(f"Loading model from best run: {best_run.info.run_id}")
                    model = mlflow.tensorflow.load_model(model_uri)
                    print(f"Successfully loaded model with accuracy: {best_run.data.metrics.get('test_accuracy', 'N/A')}")
                    return model
        except Exception as e2:
            print(f"Could not load from MLflow runs: {e2}")
        
        # Option 3: Load from local saved model if exists
        try:
            local_model_path = "./saved_model"
            if os.path.exists(local_model_path):
                print(f"Loading model from local path: {local_model_path}")
                model = mlflow.tensorflow.load_model(local_model_path)
                print("Successfully loaded model from local path")
                return model
        except Exception as e3:
            print(f"Could not load from local path: {e3}")
    
    raise Exception("Could not load model from any source. Please train a model first using train.py")


def preprocess_image(image_data):
    """
    Preprocess the image from canvas for model prediction.
    
    Args:
        image_data: Base64 encoded image data from canvas
        
    Returns:
        Preprocessed numpy array ready for model input
    """
    # Remove the data URL prefix
    if ',' in image_data:
        image_data = image_data.split(',')[1]
    
    # Decode base64 image
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert to grayscale
    image = image.convert('L')
    
    # Resize to 28x28
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    
    # Convert to numpy array
    image_array = np.array(image)
    
    # Invert colors (canvas is white on black, MNIST is black on white)
    image_array = 255 - image_array
    
    # Normalize to [0, 1]
    image_array = image_array.astype('float32') / 255.0
    
    # Reshape to (1, 28, 28, 1) for model input
    image_array = np.expand_dims(image_array, axis=0)
    image_array = np.expand_dims(image_array, axis=-1)
    
    return image_array


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle prediction requests.
    
    Expects JSON with 'image' field containing base64 encoded image data.
    Returns JSON with prediction results.
    """
    try:
        # Get image data from request
        data = request.get_json()
        image_data = data.get('image', '')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Preprocess image
        processed_image = preprocess_image(image_data)
        
        # Make prediction
        global model
        if model is None:
            model = load_model()
        
        predictions = model.predict(processed_image, verbose=0)
        predicted_digit = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]))
        
        # Get all probabilities
        all_probabilities = {
            str(i): float(predictions[0][i]) 
            for i in range(10)
        }
        
        return jsonify({
            'prediction': predicted_digit,
            'confidence': confidence,
            'probabilities': all_probabilities
        })
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})


if __name__ == '__main__':
    print("Starting Flask application...")
    print("Loading model...")
    
    try:
        load_model()
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Warning: Could not load model at startup: {e}")
        print("Model will be loaded on first prediction request")
    
    print("\nApplication running at: http://127.0.0.1:5000")
    print("Draw a digit and click 'Predict' to test the model!\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
