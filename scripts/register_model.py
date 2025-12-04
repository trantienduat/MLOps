"""
Helper script to register the best model to MLflow Model Registry.

This script automatically finds the best model from experiments and registers it.
"""

import mlflow
from mlflow.tracking import MlflowClient


def find_best_model():
    """Find the best model from all experiment runs."""
    print("=" * 60)
    print("Finding Best Model from Experiments")
    print("=" * 60)
    
    client = MlflowClient()
    
    # Get experiment
    experiment_name = "MNIST_Classification_Experiments"
    experiment = client.get_experiment_by_name(experiment_name)
    
    if not experiment:
        print(f"❌ Experiment '{experiment_name}' not found!")
        print("Please run train.py first to create experiments.")
        return None
    
    print(f"✓ Found experiment: {experiment_name}")
    print(f"  Experiment ID: {experiment.experiment_id}")
    
    # Search for best run
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.test_accuracy DESC"],
        max_results=10
    )
    
    if not runs:
        print("❌ No runs found in experiment!")
        return None
    
    print(f"\n✓ Found {len(runs)} runs")
    print("\nTop 3 runs:")
    print("-" * 60)
    
    for i, run in enumerate(runs[:3], 1):
        accuracy = run.data.metrics.get('test_accuracy', 0)
        loss = run.data.metrics.get('test_loss', 0)
        run_name = run.data.tags.get('mlflow.runName', 'Unknown')
        print(f"{i}. {run_name}")
        print(f"   Accuracy: {accuracy:.4f} | Loss: {loss:.4f}")
        print(f"   Run ID: {run.info.run_id}")
        print()
    
    best_run = runs[0]
    return best_run


def register_model(run, model_name="Mnist_Best_Model"):
    """Register a model to MLflow Model Registry."""
    client = MlflowClient()
    
    # Check if model already exists
    try:
        registered_model = client.get_registered_model(model_name)
        print(f"\n⚠️  Model '{model_name}' already exists!")
        print(f"   Current versions: {len(registered_model.latest_versions)}")
        
        response = input("Do you want to create a new version? (y/n): ")
        if response.lower() != 'y':
            print("Registration cancelled.")
            return None
    except:
        print(f"\n✓ Model '{model_name}' does not exist yet. Creating...")
    
    # Register model
    model_uri = f"runs:/{run.info.run_id}/model"
    
    print(f"\nRegistering model from run: {run.info.run_id}")
    print(f"Model URI: {model_uri}")
    
    try:
        model_version = mlflow.register_model(
            model_uri=model_uri,
            name=model_name
        )
        
        print(f"\n✅ Model registered successfully!")
        print(f"   Name: {model_name}")
        print(f"   Version: {model_version.version}")
        
        # Transition to Production
        print(f"\nTransitioning version {model_version.version} to Production...")
        client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage="Production",
            archive_existing_versions=True
        )
        
        print(f"✅ Model transitioned to Production stage!")
        
        return model_version
        
    except Exception as e:
        print(f"❌ Error registering model: {e}")
        return None


def main():
    """Main function."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "MLflow Model Registration Helper" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Find best model
    best_run = find_best_model()
    
    if not best_run:
        return 1
    
    # Show best model details
    print("\n" + "=" * 60)
    print("Best Model Details")
    print("=" * 60)
    run_name = best_run.data.tags.get('mlflow.runName', 'Unknown')
    accuracy = best_run.data.metrics.get('test_accuracy', 0)
    loss = best_run.data.metrics.get('test_loss', 0)
    
    print(f"Run Name: {run_name}")
    print(f"Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Test Loss: {loss:.4f}")
    print(f"Run ID: {best_run.info.run_id}")
    
    # Ask for confirmation
    print("\n" + "-" * 60)
    response = input("Register this model to Model Registry? (y/n): ")
    
    if response.lower() != 'y':
        print("Registration cancelled.")
        return 0
    
    # Register model
    model_version = register_model(best_run)
    
    if model_version:
        print("\n" + "=" * 60)
        print("Next Steps:")
        print("=" * 60)
        print("1. View model in MLflow UI: http://127.0.0.1:5000")
        print("2. Click 'Models' tab to see registered model")
        print("3. Run web app: python app.py")
        print("=" * 60)
        return 0
    else:
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
