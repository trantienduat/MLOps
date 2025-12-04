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

[...full content from original app.py...]
