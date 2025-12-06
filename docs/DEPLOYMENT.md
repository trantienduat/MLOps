# Deployment Guide

> **Production deployment guide for the MNIST MLOps system**

---

## Table of Contents
1. [Deployment Options](#deployment-options)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Docker Compose](#docker-compose)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Cloud Deployments](#cloud-deployments)
7. [CI/CD Pipeline](#cicd-pipeline)
8. [Monitoring](#monitoring)
9. [Troubleshooting](#troubleshooting)

---

## Deployment Options

### Overview

| Environment | Use Case | Complexity | Cost |
|-------------|----------|------------|------|
| **Local** | Development, testing | Low | Free |
| **Docker** | Local production simulation | Medium | Free |
| **Docker Compose** | Multi-service local deployment | Medium | Free |
| **Kubernetes** | Production orchestration | High | Variable |
| **Cloud (AWS/GCP/Azure)** | Scalable production | High | $$ |

---

## Local Development

### Prerequisites

- Python 3.11+
- Virtual environment
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/trantienduat/MLOps.git
cd MLOps

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Setup pre-commit hooks
pre-commit install
```

### Run Services

**MLflow Tracking Server**:
```bash
mlflow ui --host 0.0.0.0 --port 5000
# Open: http://localhost:5000
```

**API Server (Development)**:
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
# Open: http://localhost:8000
# Docs: http://localhost:8000/api/docs
```

**Training**:
```bash
python src/training/train.py
```

---

## Docker Deployment

### Build Image

```bash
# Build with default tag
docker build -t mlops-mnist:latest .

# Build with specific version
docker build -t mlops-mnist:v1.0.0 .

# Build without cache
docker build --no-cache -t mlops-mnist:latest .
```

### Multi-Architecture Build

```bash
# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t mlops-mnist:latest \
  --push .
```

### Run Container

**Basic**:
```bash
docker run -p 8000:8000 mlops-mnist:latest
```

**With Environment Variables**:
```bash
docker run \
  -p 8000:8000 \
  -e MLFLOW_TRACKING_URI=http://mlflow-server:5000 \
  -e MODEL_NAME=Mnist_Best_Model \
  -e LOG_LEVEL=INFO \
  mlops-mnist:latest
```

**With Volume Mounts**:
```bash
docker run \
  -p 8000:8000 \
  -v $(pwd)/mlruns:/app/mlruns \
  -v $(pwd)/.env:/app/.env \
  mlops-mnist:latest
```

**Detached Mode**:
```bash
docker run -d \
  --name mnist-api \
  -p 8000:8000 \
  --restart unless-stopped \
  mlops-mnist:latest
```

### Container Management

```bash
# View logs
docker logs mnist-api
docker logs -f mnist-api  # Follow logs

# Stop container
docker stop mnist-api

# Start container
docker start mnist-api

# Restart container
docker restart mnist-api

# Remove container
docker rm mnist-api

# Execute command in container
docker exec -it mnist-api bash
```

### Push to Docker Hub

```bash
# Login
docker login

# Tag image
docker tag mlops-mnist:latest <username>/mlops-mnist:latest
docker tag mlops-mnist:latest <username>/mlops-mnist:v1.0.0

# Push
docker push <username>/mlops-mnist:latest
docker push <username>/mlops-mnist:v1.0.0
```

---

## Docker Compose

### Configuration

**Basic Setup** (`docker-compose.yml`):
```yaml
version: '3.8'

services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.9.2
    ports:
      - "5000:5000"
    command: >
      mlflow server
      --host 0.0.0.0
      --port 5000
      --backend-store-uri sqlite:///mlflow.db
      --default-artifact-root /mlflow/artifacts
    volumes:
      - mlflow-data:/mlflow
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000
      - MODEL_NAME=Mnist_Best_Model
      - LOG_LEVEL=INFO
    depends_on:
      mlflow:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  mlflow-data:
```

### Commands

**Start services**:
```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d api

# Start with rebuild
docker-compose up -d --build
```

**View logs**:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
```

**Stop services**:
```bash
# Stop all
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

**Scale services**:
```bash
# Scale API service
docker-compose up -d --scale api=3
```

### Monitoring Stack

Add monitoring services to `docker-compose.yml`:

```yaml
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    profiles:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    profiles:
      - monitoring

volumes:
  prometheus-data:
  grafana-data:
```

**Start with monitoring**:
```bash
docker-compose --profile monitoring up -d
```

---

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (minikube, EKS, GKE, AKS)
- kubectl configured
- Docker images pushed to registry

### Deployment Manifests

**Namespace** (`namespace.yaml`):
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: mlops-mnist
```

**Deployment** (`deployment.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mnist-api
  namespace: mlops-mnist
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mnist-api
  template:
    metadata:
      labels:
        app: mnist-api
    spec:
      containers:
      - name: api
        image: <username>/mlops-mnist:latest
        ports:
        - containerPort: 8000
        env:
        - name: MLFLOW_TRACKING_URI
          value: "http://mlflow-service:5000"
        - name: MODEL_NAME
          value: "Mnist_Best_Model"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

**Service** (`service.yaml`):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mnist-api-service
  namespace: mlops-mnist
spec:
  selector:
    app: mnist-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

**ConfigMap** (`configmap.yaml`):
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mnist-config
  namespace: mlops-mnist
data:
  MLFLOW_TRACKING_URI: "http://mlflow-service:5000"
  MODEL_NAME: "Mnist_Best_Model"
  LOG_LEVEL: "INFO"
```

**HorizontalPodAutoscaler** (`hpa.yaml`):
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mnist-api-hpa
  namespace: mlops-mnist
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mnist-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f kubernetes/namespace.yaml

# Deploy application
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/hpa.yaml

# Or deploy all at once
kubectl apply -f kubernetes/

# Check status
kubectl get all -n mlops-mnist

# View logs
kubectl logs -n mlops-mnist deployment/mnist-api -f

# Scale manually
kubectl scale -n mlops-mnist deployment/mnist-api --replicas=5

# Update image
kubectl set image -n mlops-mnist deployment/mnist-api \
  api=<username>/mlops-mnist:v2.0.0

# Rollback
kubectl rollout undo -n mlops-mnist deployment/mnist-api
```

---

## Cloud Deployments

### AWS ECS (Elastic Container Service)

**Create Task Definition**:
```json
{
  "family": "mnist-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "<account>.dkr.ecr.<region>.amazonaws.com/mlops-mnist:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "MLFLOW_TRACKING_URI",
          "value": "http://mlflow-lb.internal:5000"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ]
}
```

**Deploy with AWS CLI**:
```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster mlops-cluster \
  --service-name mnist-api \
  --task-definition mnist-api:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Google Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/mlops-mnist

# Deploy to Cloud Run
gcloud run deploy mnist-api \
  --image gcr.io/PROJECT_ID/mlops-mnist \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MLFLOW_TRACKING_URI=http://mlflow-service:5000 \
  --memory 1Gi \
  --cpu 1 \
  --min-instances 1 \
  --max-instances 10
```

### Azure Container Instances

```bash
# Create resource group
az group create --name mlops-rg --location eastus

# Create container
az container create \
  --resource-group mlops-rg \
  --name mnist-api \
  --image <username>/mlops-mnist:latest \
  --dns-name-label mnist-api-unique \
  --ports 8000 \
  --environment-variables \
    MLFLOW_TRACKING_URI=http://mlflow:5000 \
    MODEL_NAME=Mnist_Best_Model \
  --cpu 1 \
  --memory 1
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

**File**: `.github/workflows/docker-image.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install black isort flake8 mypy
      - name: Lint
        run: |
          black --check .
          isort --check .
          flake8 .
          mypy src/

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build-and-push:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/mlops-mnist:latest
            ${{ secrets.DOCKER_USERNAME }}/mlops-mnist:${{ github.sha }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Add your deployment script here
          echo "Deploying to production..."
```

### Setup Secrets

1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Add secrets:
   - `DOCKER_USERNAME`: Docker Hub username
   - `DOCKER_PASSWORD`: Docker Hub access token

---

## Monitoring

### Prometheus Setup

**Configuration** (`prometheus.yml`):
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'mnist-api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'
```

### Grafana Dashboard

**Import Dashboard**:
1. Open Grafana (http://localhost:3000)
2. Login (admin/admin)
3. Add Prometheus data source (http://prometheus:9090)
4. Import dashboard (ID: 1860 for Node Exporter)
5. Create custom dashboard for ML metrics

**Key Metrics to Monitor**:
- Request rate (predictions/second)
- Latency percentiles (p50, p95, p99)
- Error rate
- Model confidence distribution
- Active requests

---

## Troubleshooting

### Common Issues

**Issue**: Container fails to start
```bash
# Check logs
docker logs <container-id>

# Check events
kubectl describe pod <pod-name> -n mlops-mnist
```

**Issue**: Cannot connect to MLflow
```bash
# Check MLflow service
docker-compose ps mlflow
kubectl get svc -n mlops-mnist

# Test connectivity
docker exec -it <api-container> curl http://mlflow:5000/health
```

**Issue**: High memory usage
```bash
# Check resources
docker stats
kubectl top pod -n mlops-mnist

# Increase limits in deployment
resources:
  limits:
    memory: "2Gi"
```

**Issue**: Slow predictions
```bash
# Enable model caching
# Use GPU acceleration
# Scale horizontally
```

### Health Checks

**Container health**:
```bash
curl http://localhost:8000/health
```

**MLflow health**:
```bash
curl http://localhost:5000/health
```

**Prometheus health**:
```bash
curl http://localhost:9090/-/healthy
```

---

## Security Checklist

- [ ] Environment variables for secrets
- [ ] Non-root container user
- [ ] Image vulnerability scanning
- [ ] HTTPS/TLS enabled
- [ ] API authentication configured
- [ ] Rate limiting enabled
- [ ] Network policies configured
- [ ] Regular dependency updates
- [ ] Secrets rotation schedule
- [ ] Audit logging enabled

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**For More Info**: See [ARCHITECTURE.md](ARCHITECTURE.md) for system design
