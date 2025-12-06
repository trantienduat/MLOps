# API Documentation

> **REST API documentation for MNIST prediction service**

---

## Table of Contents
1. [Overview](#overview)
2. [Base URL](#base-url)
3. [Authentication](#authentication)
4. [Endpoints](#endpoints)
5. [Data Models](#data-models)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Examples](#examples)

---

## Overview

The MNIST API provides real-time digit classification using a production-grade convolutional neural network. The API is built with FastAPI, offering automatic OpenAPI documentation, request validation, and high performance.

**Features:**
- RESTful design
- JSON request/response
- Automatic request validation
- Interactive API documentation (Swagger UI)
- Prometheus metrics exposition
- Health check endpoints

---

## Base URL

**Development:**
```
http://localhost:8000
```

**Production:**
```
https://your-domain.com/api
```

---

## Authentication

**Current**: No authentication required (development)

**Future**: API key authentication for production
```http
Authorization: Bearer <api_key>
```

---

## Endpoints

### 1. Health Check

**Endpoint**: `GET /health`

**Description**: Check API and model health status

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "Mnist_Best_Model",
  "model_version": "1"
}
```

**Status Codes:**
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is degraded

**Example**:
```bash
curl http://localhost:8000/health
```

---

### 2. Digit Prediction

**Endpoint**: `POST /predict`

**Description**: Predict digit from image

**Request Headers:**
```http
Content-Type: application/json
```

**Request Body**:
```json
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

**Response**:
```json
{
  "prediction": 5,
  "confidence": 0.9876,
  "probabilities": [
    0.0001,  // digit 0
    0.0002,  // digit 1
    0.0003,  // digit 2
    0.0004,  // digit 3
    0.0005,  // digit 4
    0.9876,  // digit 5 (predicted)
    0.0006,  // digit 6
    0.0007,  // digit 7
    0.0008,  // digit 8
    0.0009   // digit 9
  ]
}
```

**Status Codes:**
- `200 OK`: Successful prediction
- `400 Bad Request`: Invalid input
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Model error

**Example**:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg..."
  }'
```

---

### 3. Web Interface

**Endpoint**: `GET /`

**Description**: Interactive web UI for drawing and prediction

**Response**: HTML page with canvas

**Example**:
```bash
# Open in browser
http://localhost:8000/
```

---

### 4. Metrics

**Endpoint**: `GET /metrics`

**Description**: Prometheus metrics in text format

**Response**:
```
# HELP predictions_total Total number of predictions
# TYPE predictions_total counter
predictions_total{model_version="1",prediction_class="5"} 42.0

# HELP prediction_latency_seconds Time spent processing prediction
# TYPE prediction_latency_seconds histogram
prediction_latency_seconds_bucket{le="0.01"} 120.0
prediction_latency_seconds_bucket{le="0.05"} 250.0
prediction_latency_seconds_count 300.0
prediction_latency_seconds_sum 4.5

# HELP prediction_confidence Model confidence score
# TYPE prediction_confidence gauge
prediction_confidence 0.9876
```

**Example**:
```bash
curl http://localhost:8000/metrics
```

---

### 5. API Documentation

**Swagger UI**: `GET /api/docs`  
**ReDoc**: `GET /api/redoc`

**Description**: Interactive API documentation

**Example**:
```bash
# Open in browser
http://localhost:8000/api/docs
```

---

## Data Models

### PredictionRequest

**Schema**:
```json
{
  "image": "string (base64 encoded image data)"
}
```

**Fields**:
- `image` (required): Base64-encoded image with data URI prefix
  - Format: `data:image/png;base64,<base64_data>`
  - Recommended size: 28×28 pixels
  - Color: Grayscale or RGB (will be converted)

**Validation**:
- Image must be base64 encoded
- Must include data URI prefix
- Image should be clear and centered for best results

---

### PredictionResponse

**Schema**:
```json
{
  "prediction": "integer",
  "confidence": "float",
  "probabilities": ["float"]
}
```

**Fields**:
- `prediction` (integer): Predicted digit (0-9)
- `confidence` (float): Confidence score for predicted class (0.0-1.0)
- `probabilities` (array): Probability for each class [0-9]

**Example**:
```json
{
  "prediction": 7,
  "confidence": 0.9923,
  "probabilities": [
    0.0001, 0.0002, 0.0003, 0.0004, 0.0005,
    0.0006, 0.0007, 0.9923, 0.0008, 0.0009
  ]
}
```

---

### HealthResponse

**Schema**:
```json
{
  "status": "string",
  "model_loaded": "boolean",
  "model_name": "string",
  "model_version": "string"
}
```

**Fields**:
- `status`: "healthy" or "degraded"
- `model_loaded`: Whether ML model is loaded
- `model_name`: Name of loaded model
- `model_version`: Version of loaded model

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message description"
}
```

### Common Errors

**400 Bad Request**
```json
{
  "detail": "Invalid image format. Expected base64 encoded image."
}
```

**422 Validation Error**
```json
{
  "detail": [
    {
      "loc": ["body", "image"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error**
```json
{
  "detail": "Model inference failed. Please try again."
}
```

---

## Rate Limiting

**Current**: No rate limiting (development)

**Future**: Rate limiting for production
- 100 requests per minute per IP
- 1000 requests per hour per IP

**Headers**:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

---

## Examples

### Python Example

```python
import requests
import base64

# Read and encode image
with open('digit.png', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

# Create request
url = 'http://localhost:8000/predict'
payload = {
    'image': f'data:image/png;base64,{image_data}'
}

# Make request
response = requests.post(url, json=payload)
result = response.json()

print(f"Predicted digit: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")
```

---

### JavaScript Example

```javascript
// Get image from canvas
const canvas = document.getElementById('canvas');
const imageData = canvas.toDataURL('image/png');

// Make request
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    image: imageData
  })
})
.then(response => response.json())
.then(data => {
  console.log('Prediction:', data.prediction);
  console.log('Confidence:', data.confidence);
  console.log('Probabilities:', data.probabilities);
})
.catch(error => {
  console.error('Error:', error);
});
```

---

### cURL Example

```bash
# Health check
curl http://localhost:8000/health

# Prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
}
EOF

# Metrics
curl http://localhost:8000/metrics
```

---

### Postman Collection

**Import URL**:
```
https://www.postman.com/collections/<collection_id>
```

**Collection Structure**:
- GET Health Check
- POST Predict Digit
- GET Metrics
- GET API Docs

---

## Performance

### Latency

**Typical Response Times**:
- Health check: <5ms
- Prediction: 10-50ms
  - Model inference: 5-10ms
  - Image preprocessing: 1-5ms
  - Network overhead: 5-35ms

**Optimization**:
- Model loaded at startup (singleton)
- Async endpoints for I/O operations
- Efficient image preprocessing
- Response caching (future)

### Throughput

**Single Instance**:
- ~100-200 requests/second (CPU)
- ~500-1000 requests/second (GPU)

**Scaled Deployment**:
- Linear scaling with replicas
- Load balancer required

---

## Monitoring

### Prometheus Metrics

**Counter Metrics**:
- `predictions_total`: Total predictions by class
- `api_requests_total`: Total API requests by endpoint
- `prediction_errors_total`: Total prediction errors by type

**Histogram Metrics**:
- `prediction_latency_seconds`: Prediction latency distribution
- `request_duration_seconds`: Request duration distribution

**Gauge Metrics**:
- `prediction_confidence`: Current prediction confidence
- `active_requests`: Number of active requests

### Metrics Endpoint

```bash
# Scrape metrics
curl http://localhost:8000/metrics

# Prometheus config
scrape_configs:
  - job_name: 'mnist-api'
    static_configs:
      - targets: ['localhost:8000']
```

---

## OpenAPI Specification

**Download OpenAPI spec**:
```bash
curl http://localhost:8000/openapi.json > openapi.json
```

**Spec includes**:
- All endpoints
- Request/response schemas
- Validation rules
- Example payloads
- Error responses

**Use with**:
- Code generation tools
- API testing tools
- Documentation generators

---

## Best Practices

### Client Implementation

**Do**:
- ✅ Handle errors gracefully
- ✅ Implement retry logic with exponential backoff
- ✅ Validate responses
- ✅ Use connection pooling
- ✅ Set appropriate timeouts

**Don't**:
- ❌ Send extremely large images
- ❌ Retry indefinitely
- ❌ Hardcode URLs (use config)
- ❌ Ignore error responses
- ❌ Skip input validation

### Image Preparation

**Recommendations**:
- Use 28×28 pixel images
- Center the digit
- Use dark digit on light background
- Avoid noise and artifacts
- Ensure good contrast

**Pre-processing**:
```python
from PIL import Image
import numpy as np

# Load and resize
img = Image.open('digit.png').convert('L')  # Grayscale
img = img.resize((28, 28))

# Normalize
img_array = np.array(img) / 255.0

# Invert if needed (MNIST uses white on black)
if img_array.mean() > 0.5:
    img_array = 1 - img_array
```

---

## Testing

### Unit Testing

```python
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict():
    payload = {
        "image": "data:image/png;base64,..."
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
```

### Integration Testing

```python
import requests

def test_end_to_end():
    # Create test image
    image_data = create_test_digit_image(digit=5)
    
    # Make prediction
    response = requests.post(
        "http://localhost:8000/predict",
        json={"image": image_data}
    )
    
    # Verify response
    assert response.status_code == 200
    result = response.json()
    assert result["prediction"] == 5
    assert result["confidence"] > 0.9
```

---

## Changelog

### Version 1.0 (Current)
- Initial API release
- Prediction endpoint
- Health check endpoint
- Prometheus metrics
- Web UI
- OpenAPI documentation

### Planned Features
- API key authentication
- Rate limiting
- Batch predictions
- Model versioning in API
- Response caching
- WebSocket support

---

**API Version**: 1.0  
**Last Updated**: December 2025  
**Support**: See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment guide
