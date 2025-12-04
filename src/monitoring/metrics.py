"""Prometheus metrics for model serving monitoring."""

from prometheus_client import Counter, Gauge, Histogram

# Prediction metrics
prediction_counter = Counter(
    "predictions_total",
    "Total number of predictions made",
    ["model_version", "predicted_class"],
)

prediction_latency = Histogram(
    "prediction_latency_seconds",
    "Time spent processing prediction request",
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0],
)

model_confidence = Gauge(
    "prediction_confidence",
    "Model confidence score for predictions",
)

prediction_errors = Counter(
    "prediction_errors_total",
    "Total number of prediction errors",
    ["error_type"],
)

# API metrics
api_requests = Counter(
    "api_requests_total",
    "Total number of API requests",
    ["method", "endpoint", "status_code"],
)

active_requests = Gauge(
    "active_requests",
    "Number of currently active requests",
)
