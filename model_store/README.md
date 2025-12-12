# Model Store (Baked into Image)

Place your exported MLflow model here before building the Docker image so it is baked into the runtime image. Expected layout:

```
model_store/
  README.md
  model/                  # MLflow TensorFlow artifact directory
    MLmodel
    model.keras
    ...
```

How to export a model from an MLflow run:

```bash
# Identify best run (example using MLflow CLI or UI)
# Copy its artifact directory into model_store/model
cp -r mlruns/<experiment_id>/<run_id>/artifacts/model model_store/

# Or after registering, you can also download the Production model via MLflow:
mlflow models download -m "models:/Mnist_Best_Model/Production" -d model_store/model
```

Build the image (will include the model):

```bash
docker build -t mlops-mnist:with-model .
```

At runtime, set `MODEL_LOCAL_PATH=/app/model_store/model` (already defaulted in the Dockerfile) to load the baked model without needing the registry or volumes.
