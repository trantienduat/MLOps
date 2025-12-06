# Technical Documentation

> **Enterprise MLOps MNIST Classification System - Technical Documentation**

---

## 📚 Documentation Structure

This directory contains comprehensive technical documentation for the MLOps MNIST system. The documentation is organized by topic to provide clear, focused information for different aspects of the system.

---

## 📖 Available Documentation

### [ARCHITECTURE.md](ARCHITECTURE.md)
**System Architecture and Design**

Comprehensive architecture documentation following the C4 model:
- System Context Diagram (Level 1)
- Container Diagram (Level 2)
- Component Diagram (Level 3)
- Code Organization (Level 4)
- ML Pipeline Architecture
- Technology Stack
- Data Flow
- Security Architecture
- Performance Considerations
- Deployment Patterns

**Target Audience**: Architects, Tech Leads, Senior Engineers  
**Topics**: System design, technical architecture, C4 diagrams, infrastructure

---

### [ML_PIPELINE.md](ML_PIPELINE.md)
**Machine Learning Training Pipeline**

Detailed documentation of the ML training pipeline:
- Dataset Characteristics (MNIST)
- Data Preprocessing
- Model Architectures (3 runs)
- Training Strategy & Hyperparameters
- Experiment Tracking with MLflow
- Model Evaluation Metrics
- Best Practices for ML Development
- Code Examples
- Performance Benchmarks
- Troubleshooting

**Target Audience**: Data Scientists, ML Engineers  
**Topics**: Model training, experimentation, MLflow, hyperparameter tuning

---

### [API.md](API.md)
**REST API Documentation**

Complete API reference and usage guide:
- Endpoint Documentation
  - Health Check
  - Digit Prediction
  - Metrics Exposition
- Request/Response Schemas
- Data Models (Pydantic)
- Error Handling
- Rate Limiting (planned)
- Code Examples (Python, JavaScript, cURL)
- Performance Metrics
- OpenAPI Specification
- Best Practices

**Target Audience**: Application Developers, Frontend Engineers, API Consumers  
**Topics**: API endpoints, request/response formats, integration examples

---

### [DEPLOYMENT.md](DEPLOYMENT.md)
**Production Deployment Guide**

Comprehensive deployment strategies and operations:
- Local Development Setup
- Docker Deployment
- Docker Compose Multi-Service
- Kubernetes Deployment
  - Manifests (Deployment, Service, HPA, ConfigMap)
  - Scaling Strategies
- Cloud Deployments
  - AWS ECS
  - Google Cloud Run
  - Azure Container Instances
- CI/CD Pipeline (GitHub Actions)
- Monitoring Setup (Prometheus, Grafana)
- Troubleshooting
- Security Checklist

**Target Audience**: DevOps Engineers, SREs, Platform Engineers  
**Topics**: Deployment, operations, monitoring, CI/CD, infrastructure

---

## 🎯 Quick Navigation

### I want to...

**Understand the system architecture**
→ Read [ARCHITECTURE.md](ARCHITECTURE.md)

**Train and improve ML models**
→ Read [ML_PIPELINE.md](ML_PIPELINE.md)

**Integrate with the API**
→ Read [API.md](API.md)

**Deploy to production**
→ Read [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────┐
│         MLOps MNIST Platform                     │
│                                                  │
│  ┌────────────┐  ┌────────────┐  ┌───────────┐│
│  │ Training   │  │ API        │  │ Monitoring││
│  │ Pipeline   │  │ Service    │  │ Stack     ││
│  │            │  │            │  │           ││
│  │ TensorFlow │  │ FastAPI    │  │Prometheus ││
│  │ + MLflow   │  │ + Gunicorn │  │+ Grafana  ││
│  └────────────┘  └────────────┘  └───────────┘│
│         │                │              │       │
│         └────────────────┴──────────────┘       │
│                     │                            │
│              ┌──────▼──────┐                    │
│              │   MLflow    │                    │
│              │   Server    │                    │
│              └─────────────┘                    │
└─────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed C4 diagrams.

---

## 🔄 ML Workflow

```
Data → Preprocessing → Training → Evaluation → Registry → Serving
  │         │             │           │          │         │
  │         │             │           │          │         │
MNIST   Normalize    3 Experiments  Compare   MLflow   FastAPI
        Reshape      (Runs 1-3)    Metrics   Models   Endpoint
```

See [ML_PIPELINE.md](ML_PIPELINE.md) for detailed workflow.

---

## 🌐 API Endpoints

```
GET  /health          → Health check
POST /predict         → Digit prediction
GET  /                → Web UI
GET  /metrics         → Prometheus metrics
GET  /api/docs        → Swagger UI
GET  /api/redoc       → ReDoc UI
```

See [API.md](API.md) for complete API reference.

---

## 🚀 Deployment Options

| Environment | Documentation | Complexity | Production-Ready |
|-------------|---------------|------------|------------------|
| Local Development | [DEPLOYMENT.md](DEPLOYMENT.md#local-development) | Low | No |
| Docker | [DEPLOYMENT.md](DEPLOYMENT.md#docker-deployment) | Medium | Yes |
| Docker Compose | [DEPLOYMENT.md](DEPLOYMENT.md#docker-compose) | Medium | Yes |
| Kubernetes | [DEPLOYMENT.md](DEPLOYMENT.md#kubernetes-deployment) | High | Yes |
| Cloud (AWS/GCP/Azure) | [DEPLOYMENT.md](DEPLOYMENT.md#cloud-deployments) | High | Yes |

---

## 🛠️ Technology Stack

**Core Technologies:**
- **ML Framework**: TensorFlow 2.15+
- **Experiment Tracking**: MLflow 2.9+
- **API Framework**: FastAPI 0.109+
- **Server**: Gunicorn + Uvicorn
- **Monitoring**: Prometheus + Grafana
- **Container**: Docker + Docker Compose
- **Orchestration**: Kubernetes (production)

See [ARCHITECTURE.md](ARCHITECTURE.md#technology-stack) for complete stack.

---

## 📊 Model Performance

| Run | Architecture | Test Accuracy | Purpose |
|-----|--------------|---------------|---------|
| 1 | Baseline CNN | ~98.0% | Establish baseline |
| 2 | Enhanced CNN | ~98.5% | Improve architecture |
| 3 | Optimized | ~99.0%+ | Tune hyperparameters |

See [ML_PIPELINE.md](ML_PIPELINE.md#expected-results) for details.

---

## 🔒 Security

**Multi-Layer Security:**
- Container security (non-root, multi-stage build)
- Dependency scanning (safety, pip-audit)
- Image scanning (Trivy)
- Input validation (Pydantic)
- Secrets management (.env, GitHub Secrets)
- Network isolation
- HTTPS ready

See [ARCHITECTURE.md](ARCHITECTURE.md#security-architecture) for security details.

---

## 📈 Monitoring

**Key Metrics:**
- `predictions_total` - Counter by prediction class
- `prediction_latency_seconds` - Histogram of latency
- `prediction_confidence` - Gauge of model confidence
- `api_requests_total` - Request counter
- `active_requests` - Active request gauge

See [DEPLOYMENT.md](DEPLOYMENT.md#monitoring) for monitoring setup.

---

## 🧪 Testing

**Test Coverage:**
- Unit tests (pytest)
- Integration tests (API testing)
- End-to-end tests (pipeline testing)
- Coverage target: 80%+

**Code Quality:**
- Black (formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)
- pylint (code analysis)

See [ARCHITECTURE.md](ARCHITECTURE.md#technology-stack) for tools.

---

## 📝 Additional Resources

### External Documentation
- [MLflow Documentation](https://mlflow.org/docs/latest/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TensorFlow Guide](https://www.tensorflow.org/guide)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)

### Best Practices
- [Google MLOps Best Practices](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- [AWS Well-Architected ML Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html)
- [Microsoft MLOps](https://docs.microsoft.com/en-us/azure/machine-learning/concept-model-management-and-deployment)

---

## 🤝 Contributing

When contributing documentation:
1. Follow existing structure and format
2. Include code examples where appropriate
3. Add diagrams for complex concepts
4. Update this README if adding new docs
5. Keep language clear and concise
6. Focus on technical accuracy

---

## 📞 Support

For questions about:
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **ML Pipeline**: See [ML_PIPELINE.md](ML_PIPELINE.md)
- **API Integration**: See [API.md](API.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)

For issues not covered in documentation, please open a GitHub issue.

---

**Documentation Version**: 1.0  
**Last Updated**: December 2025  
**Maintained By**: MLOps Team

---

**Quick Links:**
- [Main README](../README.md)
- [GitHub Repository](https://github.com/trantienduat/MLOps)
- [Project Guidelines](../.github/copilot-instructions.md)
