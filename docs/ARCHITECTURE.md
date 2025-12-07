# Enterprise MLOps Architecture

> **Technical architecture documentation for the MNIST MLOps system following C4 model principles**

---

## Table of Contents
1. [System Overview](#system-overview)
2. [C4 Architecture Model](#c4-architecture-model)
3. [ML Pipeline Architecture](#ml-pipeline-architecture)
4. [Technology Stack](#technology-stack)
5. [Data Flow](#data-flow)
6. [Security Architecture](#security-architecture)

---

## System Overview

The MNIST MLOps system is an enterprise-grade machine learning platform demonstrating production-ready practices for model development, deployment, and monitoring. The system implements a complete MLOps lifecycle from data ingestion to model serving with comprehensive observability.

**Key Architectural Principles:**
- **Separation of Concerns**: Training, serving, and monitoring are isolated services
- **Microservices Architecture**: Each component is independently deployable
- **Event-Driven Design**: Async operations for scalability
- **API-First**: RESTful interfaces with OpenAPI specifications
- **Cloud-Native**: Container-based with orchestration support

---

## C4 Architecture Model

### Level 1: System Context Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         System Context                               │
│                                                                      │
│                                                                      │
│   ┌──────────────┐                                                  │
│   │              │                                                  │
│   │  Data        │                                                  │
│   │  Scientist   │───────┐                                         │
│   │              │       │                                         │
│   └──────────────┘       │                                         │
│                          │   Train Models                          │
│                          │   View Experiments                      │
│                          ▼                                         │
│              ┌─────────────────────────┐                           │
│              │                         │                           │
│              │  MNIST MLOps Platform   │◄───────────┐             │
│              │                         │            │             │
│              │  - Model Training       │            │             │
│              │  - Experiment Tracking  │            │ Make        │
│              │  - Model Serving        │            │ Predictions │
│              │  - Monitoring           │            │             │
│              │                         │            │             │
│              └─────────────────────────┘            │             │
│                          │                          │             │
│                          │                          │             │
│                          │   Store Metrics    ┌─────────────┐    │
│                          └────────────────────►│             │    │
│                                                │  End User   │────┘
│              ┌─────────────────────────┐      │  (Web/API)  │
│              │                         │      │             │
│              │   MLflow Server         │      └─────────────┘
│              │   (External)            │
│              │                         │      ┌─────────────┐
│              └─────────────────────────┘      │             │
│                                                │ Prometheus  │
│              ┌─────────────────────────┐      │ (Monitoring)│
│              │                         │◄─────│             │
│              │   Docker Hub            │      └─────────────┘
│              │   (Container Registry)  │
│              │                         │
│              └─────────────────────────┘
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**External Systems:**
- **MLflow Server**: Experiment tracking and model registry
- **Docker Hub**: Container image repository
- **Prometheus**: Metrics collection and monitoring

---

### Level 2: Container Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          MLOps Platform Containers                        │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Training Container                            │   │
│  │                                                                  │   │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │   │
│  │   │              │    │              │    │              │    │   │
│  │   │ Data Loader  │───►│ CNN Model    │───►│ MLflow       │    │   │
│  │   │              │    │ Training     │    │ Integration  │    │   │
│  │   │              │    │              │    │              │    │   │
│  │   └──────────────┘    └──────────────┘    └──────────────┘    │   │
│  │                                                 │               │   │
│  │   Technology: Python 3.11, TensorFlow 2.15     │               │   │
│  │                                                 │               │   │
│  └─────────────────────────────────────────────────┼───────────────┘   │
│                                                     │                    │
│                                                     │ HTTP/REST          │
│                                                     ▼                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                MLflow Tracking Server (External)                 │   │
│  │                                                                  │   │
│  │   • Experiment Tracking                                         │   │
│  │   • Model Registry                                              │   │
│  │   • Artifact Storage                                            │   │
│  │   • Model Versioning                                            │   │
│  │                                                                  │   │
│  │   Technology: MLflow 2.9+, SQLite/PostgreSQL                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                     │                    │
│                                                     │                    │
│                                                     ▼                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    API Service Container                         │   │
│  │                                                                  │   │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │   │
│  │   │              │    │              │    │              │    │   │
│  │   │ FastAPI      │───►│ Model Loader │───►│ Prediction   │    │   │
│  │   │ Endpoints    │    │              │    │ Service      │    │   │
│  │   │              │    │              │    │              │    │   │
│  │   └──────┬───────┘    └──────────────┘    └──────────────┘    │   │
│  │          │                                                      │   │
│  │          │                                                      │   │
│  │          ▼                                                      │   │
│  │   ┌──────────────┐    ┌──────────────┐                        │   │
│  │   │              │    │              │                        │   │
│  │   │ Prometheus   │    │ Health Check │                        │   │
│  │   │ Metrics      │    │              │                        │   │
│  │   │              │    │              │                        │   │
│  │   └──────────────┘    └──────────────┘                        │   │
│  │                                                                  │   │
│  │   Technology: FastAPI, Gunicorn + Uvicorn                      │   │
│  │   Port: 8000                                                    │   │
│  └──────────────────────────────────────────────────┬───────────────┘   │
│                                                      │                   │
│                                                      │ /metrics          │
│                                                      ▼                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │              Prometheus Monitoring (Optional)                    │   │
│  │                                                                  │   │
│  │   • Metrics Collection                                          │   │
│  │   • Time-Series Database                                        │   │
│  │   • Alerting Rules                                              │   │
│  │                                                                  │   │
│  │   Technology: Prometheus                                        │   │
│  │   Port: 9090                                                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

**Container Responsibilities:**

1. **Training Container**
   - Data preprocessing and augmentation
   - Model architecture definition
   - Training loop execution
   - Experiment logging to MLflow
   - Model artifact storage

2. **API Service Container**
   - RESTful API endpoints
   - Model loading from registry
   - Real-time inference
   - Request validation (Pydantic)
   - Metrics exposition

3. **MLflow Server** (External)
   - Centralized experiment tracking
   - Model versioning and registry
   - Artifact storage (models, plots, logs)
   - Model stage transitions (None → Staging → Production)

4. **Prometheus** (Optional)
   - Metrics scraping from API service
   - Time-series data storage
   - Query interface for metrics
   - Alert rule evaluation

---

### Level 3: Component Diagram - API Service

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FastAPI Service Components                       │
│                                                                         │
│  HTTP Request                                                           │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────┐          │
│  │              Middleware Layer                            │          │
│  │                                                          │          │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────────┐      │          │
│  │  │   CORS    │  │  Request  │  │  Error        │      │          │
│  │  │ Middleware│  │  Tracking │  │  Handler      │      │          │
│  │  └───────────┘  └───────────┘  └───────────────┘      │          │
│  └─────────────────────────────────────────────────────────┘          │
│       │                                                                 │
│       ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────┐          │
│  │              API Router Layer                            │          │
│  │                                                          │          │
│  │  ┌────────────────┐  ┌────────────────┐  ┌───────────┐│          │
│  │  │                │  │                │  │           ││          │
│  │  │ GET /health    │  │ POST /predict  │  │ GET /     ││          │
│  │  │                │  │                │  │ (Web UI)  ││          │
│  │  └────────┬───────┘  └────────┬───────┘  └───────────┘│          │
│  │           │                    │                        │          │
│  └───────────┼────────────────────┼────────────────────────┘          │
│              │                    │                                    │
│              ▼                    ▼                                    │
│  ┌─────────────────────┐  ┌─────────────────────────────┐           │
│  │  Health Check       │  │  Prediction Service         │           │
│  │  Component          │  │                             │           │
│  │                     │  │  ┌──────────────────┐      │           │
│  │  • Model Status     │  │  │ Request Schema   │      │           │
│  │  • System Health    │  │  │ Validation       │      │           │
│  │  • Dependency Check │  │  │ (Pydantic)       │      │           │
│  └─────────────────────┘  │  └─────────┬────────┘      │           │
│                            │            │                │           │
│                            │            ▼                │           │
│  ┌─────────────────────┐  │  ┌──────────────────┐      │           │
│  │  Configuration      │  │  │ Image            │      │           │
│  │  Manager            │  │  │ Preprocessing    │      │           │
│  │                     │  │  └─────────┬────────┘      │           │
│  │  • Environment Vars │  │            │                │           │
│  │  • Model Paths      │  │            ▼                │           │
│  │  • API Settings     │  │  ┌──────────────────┐      │           │
│  └─────────────────────┘  │  │ Model Inference  │      │           │
│                            │  │                  │      │           │
│                            │  └─────────┬────────┘      │           │
│  ┌─────────────────────┐  │            │                │           │
│  │  Logging Service    │  │            ▼                │           │
│  │                     │  │  ┌──────────────────┐      │           │
│  │  • Structured Logs  │  │  │ Response Schema  │      │           │
│  │  • Log Levels       │  │  │ Formatting       │      │           │
│  │  • JSON Format      │  │  │ (Pydantic)       │      │           │
│  └─────────────────────┘  │  └──────────────────┘      │           │
│                            └─────────────────────────────┘           │
│              │                                                        │
│              ▼                                                        │
│  ┌─────────────────────────────────────────────────────┐            │
│  │              Metrics Layer (Prometheus)              │            │
│  │                                                      │            │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │            │
│  │  │ Counter:     │  │ Histogram:   │  │ Gauge:   │ │            │
│  │  │ predictions  │  │ latency      │  │ confidence│ │            │
│  │  │ _total       │  │              │  │          │ │            │
│  │  └──────────────┘  └──────────────┘  └──────────┘ │            │
│  │                                                      │            │
│  │  Exposed at: GET /metrics (Prometheus format)       │            │
│  └─────────────────────────────────────────────────────┘            │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**Component Details:**

1. **Middleware Layer**
   - CORS: Cross-origin resource sharing
   - Request tracking: Unique request IDs
   - Error handling: Global exception handlers

2. **API Router**
   - `/health`: Health check endpoint with model status
   - `/predict`: Prediction endpoint with request validation
   - `/`: Web UI serving
   - `/metrics`: Prometheus metrics exposition

3. **Services**
   - **Prediction Service**: Core ML inference logic
   - **Configuration Manager**: Centralized config (`.env` + defaults)
   - **Logging Service**: Structured logging with JSON output

4. **Data Models (Pydantic)**
   - `PredictionRequest`: Input validation schema
   - `PredictionResponse`: Output formatting schema
   - `HealthResponse`: Health check response

---

### Level 4: Code Organization

```
src/
├── api/                      # API Service
│   ├── main.py              # FastAPI app, routes, middleware
│   └── schemas.py           # Pydantic models
│
├── models/                   # ML Model Architectures
│   └── cnn.py               # CNN model definitions (3 variants)
│
├── data/                     # Data Processing
│   └── loader.py            # MNIST data loading & preprocessing
│
├── training/                 # Training Pipeline
│   └── train.py             # Training orchestration, MLflow integration
│
├── monitoring/               # Observability
│   └── metrics.py           # Prometheus metrics definitions
│
└── utils/                    # Shared Utilities
    ├── config.py            # Configuration management
    └── logger.py            # Logging setup
```

---

## ML Pipeline Architecture

### Training Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                      ML Training Pipeline                            │
│                                                                      │
│  1. Data Acquisition                                                 │
│     │                                                                │
│     │   ┌──────────────────────────────────────┐                   │
│     └──►│  MNIST Dataset Loader                │                   │
│         │  • Download from keras.datasets      │                   │
│         │  • Train: 60,000 images (28x28)      │                   │
│         │  • Test: 10,000 images                │                   │
│         └────────────┬─────────────────────────┘                   │
│                      │                                               │
│  2. Data Preprocessing                                               │
│                      │                                               │
│         ┌────────────▼─────────────────────────┐                   │
│         │  Preprocessing Pipeline              │                   │
│         │  • Normalize: [0, 255] → [0, 1]     │                   │
│         │  • Reshape: (28, 28) → (28, 28, 1)  │                   │
│         │  • One-hot encode labels             │                   │
│         └────────────┬─────────────────────────┘                   │
│                      │                                               │
│  3. Model Architecture Selection                                    │
│                      │                                               │
│         ┌────────────▼─────────────────────────┐                   │
│         │  Model Builder                       │                   │
│         │                                       │                   │
│         │  ┌────────┐  ┌────────┐  ┌────────┐│                   │
│         │  │ Run 1  │  │ Run 2  │  │ Run 3  ││                   │
│         │  │Baseline│  │Enhanced│  │Optimized│                   │
│         │  └───┬────┘  └───┬────┘  └───┬────┘│                   │
│         └──────┼───────────┼───────────┼──────┘                   │
│                │           │           │                           │
│  4. Training Execution                                              │
│                │           │           │                           │
│         ┌──────▼───────────▼───────────▼──────┐                   │
│         │  Training Loop (per run)             │                   │
│         │  • Batch processing                  │                   │
│         │  • Forward pass                      │                   │
│         │  • Loss calculation                  │                   │
│         │  • Backward propagation              │                   │
│         │  • Optimizer step                    │                   │
│         │  • Metrics logging per epoch         │                   │
│         └────────────┬─────────────────────────┘                   │
│                      │                                               │
│  5. Experiment Tracking                                             │
│                      │                                               │
│         ┌────────────▼─────────────────────────┐                   │
│         │  MLflow Integration                  │                   │
│         │                                       │                   │
│         │  • Log hyperparameters               │                   │
│         │  • Log metrics (accuracy, loss)      │                   │
│         │  • Log model artifacts               │                   │
│         │  • Log training curves               │                   │
│         │  • Tag runs                          │                   │
│         └────────────┬─────────────────────────┘                   │
│                      │                                               │
│  6. Model Evaluation                                                │
│                      │                                               │
│         ┌────────────▼─────────────────────────┐                   │
│         │  Test Set Evaluation                 │                   │
│         │  • Calculate test accuracy           │                   │
│         │  • Calculate test loss               │                   │
│         │  • Generate confusion matrix         │                   │
│         │  • Log final metrics to MLflow       │                   │
│         └────────────┬─────────────────────────┘                   │
│                      │                                               │
│  7. Model Registration                                              │
│                      │                                               │
│         ┌────────────▼─────────────────────────┐                   │
│         │  Model Registry                      │                   │
│         │  • Select best run (by accuracy)     │                   │
│         │  • Register model with MLflow        │                   │
│         │  • Transition to Production stage    │                   │
│         │  • Tag with metadata                 │                   │
│         └──────────────────────────────────────┘                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Three-Run Experiment Strategy

**Purpose**: Systematic model improvement through controlled experimentation

```
┌──────────────────────────────────────────────────────────────────────┐
│                     Experiment Progression                            │
│                                                                       │
│  Run 1: Baseline                                                     │
│  ┌────────────────────────────────────────────────────────┐         │
│  │ Architecture: Simple CNN                                │         │
│  │ • Conv2D(32 filters, 3x3)                              │         │
│  │ • MaxPooling2D(2x2)                                    │         │
│  │ • Flatten                                               │         │
│  │ • Dense(10, softmax)                                   │         │
│  │                                                         │         │
│  │ Hyperparameters:                                        │         │
│  │ • Learning Rate: 0.001                                 │         │
│  │ • Batch Size: 128                                      │         │
│  │ • Epochs: 5                                            │         │
│  │ • Optimizer: Adam                                      │         │
│  │                                                         │         │
│  │ Expected Accuracy: ~98%                                │         │
│  │ Purpose: Establish performance baseline                │         │
│  └────────────────────────────────────────────────────────┘         │
│                          │                                            │
│                          ▼                                            │
│  Run 2: Architecture Enhancement                                     │
│  ┌────────────────────────────────────────────────────────┐         │
│  │ Architecture: Enhanced CNN with Dropout                 │         │
│  │ • Conv2D(64 filters, 3x3)                              │         │
│  │ • MaxPooling2D(2x2)                                    │         │
│  │ • Dropout(0.25)                                        │         │
│  │ • Flatten                                               │         │
│  │ • Dense(128, ReLU)                                     │         │
│  │ • Dropout(0.5)                                         │         │
│  │ • Dense(10, softmax)                                   │         │
│  │                                                         │         │
│  │ Hyperparameters:                                        │         │
│  │ • Learning Rate: 0.001 (same)                          │         │
│  │ • Batch Size: 128 (same)                               │         │
│  │ • Epochs: 5 (same)                                     │         │
│  │ • Optimizer: Adam                                      │         │
│  │                                                         │         │
│  │ Expected Accuracy: ~98.5%                              │         │
│  │ Purpose: Prevent overfitting, increase capacity        │         │
│  └────────────────────────────────────────────────────────┘         │
│                          │                                            │
│                          ▼                                            │
│  Run 3: Hyperparameter Optimization                                  │
│  ┌────────────────────────────────────────────────────────┐         │
│  │ Architecture: Same as Run 2                             │         │
│  │                                                         │         │
│  │ Hyperparameters:                                        │         │
│  │ • Learning Rate: 0.0005 (reduced)                      │         │
│  │ • Batch Size: 64 (reduced)                             │         │
│  │ • Epochs: 5 (same)                                     │         │
│  │ • Optimizer: Adam                                      │         │
│  │                                                         │         │
│  │ Expected Accuracy: ~99%+                               │         │
│  │ Purpose: Optimize convergence, fine-tune performance   │         │
│  └────────────────────────────────────────────────────────┘         │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **ML Framework** | TensorFlow | 2.15.0 | Model training and inference |
| **Experiment Tracking** | MLflow | 2.9.2 | Experiment logging and model registry |
| **API Framework** | FastAPI | 0.109.0 | RESTful API with auto-docs |
| **ASGI Server** | Uvicorn | 0.27.0 | Async web server |
| **Production Server** | Gunicorn | 21.2.0 | Production WSGI server |
| **Data Validation** | Pydantic | 2.5.3 | Request/response validation |
| **Monitoring** | Prometheus Client | 0.19.0 | Metrics exposition |
| **Container Runtime** | Docker | 20.10+ | Containerization |
| **Orchestration** | Docker Compose | 2.0+ | Local multi-container deployment |

### Development Tools

| Category | Tools |
|----------|-------|
| **Code Quality** | Black, isort, flake8, pylint |
| **Type Checking** | MyPy |
| **Testing** | pytest, pytest-cov, pytest-asyncio |
| **Security** | safety, pip-audit, Trivy |
| **CI/CD** | GitHub Actions |
| **Pre-commit** | pre-commit hooks |

---

## Data Flow

### Training Data Flow

```
MNIST Dataset (Keras)
        │
        │ Download & Cache
        ▼
  Raw Images (28x28)
        │
        │ Preprocessing
        │ • Normalization
        │ • Reshaping
        │ • Label encoding
        ▼
  Processed Data
        │
        │ Training Loop
        ▼
  Model Weights
        │
        │ Serialization
        ▼
  Model Artifact (.h5)
        │
        │ MLflow Upload
        ▼
  MLflow Artifact Store
        │
        │ Registration
        ▼
  Model Registry (Production)
```

### Inference Data Flow

```
Client Request (HTTP POST)
        │
        │ API Gateway
        ▼
  Request Validation (Pydantic)
        │
        │ Base64 Decode
        ▼
  Image Data (28x28)
        │
        │ Preprocessing
        │ • Resize
        │ • Normalize
        │ • Reshape
        ▼
  Model Input Tensor
        │
        │ Inference
        ▼
  Prediction Probabilities (10 classes)
        │
        │ Post-processing
        │ • ArgMax for prediction
        │ • Confidence calculation
        ▼
  Response Formatting (Pydantic)
        │
        │ JSON Serialization
        ▼
  HTTP Response (JSON)
        │
        │ Metrics Logging
        ▼
  Prometheus Metrics
```

---

## Security Architecture

### Multi-Layer Security

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                           │
│                                                              │
│  1. Container Security                                       │
│     ┌──────────────────────────────────────────┐           │
│     │ • Multi-stage Docker build               │           │
│     │ • Non-root user (appuser:1000)           │           │
│     │ • Minimal base image (python:3.11-slim)  │           │
│     │ • Security scanning (Trivy)              │           │
│     │ • No secrets in image                    │           │
│     └──────────────────────────────────────────┘           │
│                                                              │
│  2. Dependency Security                                     │
│     ┌──────────────────────────────────────────┐           │
│     │ • Safety vulnerability scanning          │           │
│     │ • pip-audit package auditing             │           │
│     │ • Pinned versions in requirements.txt    │           │
│     │ • Automated updates via Dependabot       │           │
│     └──────────────────────────────────────────┘           │
│                                                              │
│  3. Application Security                                    │
│     ┌──────────────────────────────────────────┐           │
│     │ • Input validation (Pydantic)            │           │
│     │ • CORS configuration                     │           │
│     │ • Rate limiting (planned)                │           │
│     │ • Request size limits                    │           │
│     │ • Error sanitization                     │           │
│     └──────────────────────────────────────────┘           │
│                                                              │
│  4. Secrets Management                                      │
│     ┌──────────────────────────────────────────┐           │
│     │ • Environment variables (.env)           │           │
│     │ • GitHub Secrets for CI/CD               │           │
│     │ • No hardcoded credentials               │           │
│     │ • .env.example template only             │           │
│     └──────────────────────────────────────────┘           │
│                                                              │
│  5. Network Security                                        │
│     ┌──────────────────────────────────────────┐           │
│     │ • HTTPS ready (reverse proxy)            │           │
│     │ • Container network isolation            │           │
│     │ • Port exposure minimization             │           │
│     └──────────────────────────────────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### CI/CD Security Pipeline

```
Code Push
    │
    ▼
┌─────────────────┐
│ Lint & Format   │ ← Black, isort, flake8, mypy
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Unit Tests      │ ← pytest with coverage
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Security Scan   │ ← safety, pip-audit
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Build Container │ ← Multi-stage Docker build
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Image Scan      │ ← Trivy vulnerability scan
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Push to Registry│ ← Docker Hub with version tags
└─────────────────┘
```

---

## Performance Considerations

### Model Inference Optimization

- **Model Loading**: Singleton pattern to load model once at startup
- **Batch Processing**: Support for batch predictions (future enhancement)
- **Caching**: Model artifacts cached in memory
- **Async Processing**: FastAPI async endpoints for non-blocking I/O

### Scalability

- **Horizontal Scaling**: Stateless API enables multiple replicas
- **Load Balancing**: Compatible with standard load balancers
- **Resource Limits**: Configurable CPU/memory limits in Docker
- **Auto-scaling**: Kubernetes HPA compatible (future)

### Monitoring & Alerting

- **Metrics**: Prometheus metrics for prediction latency, throughput, accuracy
- **Health Checks**: Liveness and readiness probes
- **Logging**: Structured JSON logs for centralized log aggregation
- **Tracing**: OpenTelemetry ready (future enhancement)

---

## Deployment Patterns

### Development
```
Developer Machine
├── Python Virtual Environment (.venv)
├── MLflow UI (localhost:5000)
└── API Server (localhost:8000)
```

### Staging/Production
```
Docker Compose / Kubernetes
├── MLflow Service
│   ├── Tracking Server
│   └── Model Registry
├── API Service (N replicas)
│   ├── Gunicorn + Uvicorn
│   └── Model Serving
├── Prometheus
│   └── Metrics Collection
└── Grafana (Optional)
    └── Visualization
```

---

## Future Enhancements

- **A/B Testing**: Model version comparison in production
- **Data Drift Detection**: Evidently AI integration
- **Model Retraining**: Automated retraining triggers
- **Kubernetes Deployment**: Production-grade orchestration
- **Model Compression**: Quantization for edge deployment
- **Streaming Predictions**: WebSocket support
- **Feature Store**: Centralized feature management
- **Model Explainability**: SHAP/LIME integration

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Maintainer**: MLOps Team
