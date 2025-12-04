# MLOps Project Instructions

---

## PHASE 1: SETUP & TRAINING (3 - 4 Hours)

### PYTHON VERSION & CODING CONVENTIONS

- **Python Version:** Use Python 3.11 for the entire project (recommended: create a virtualenv with python3.11).
- **Naming Conventions & Standards:**
	- Use `snake_case` for variable and function names.
	- Use `PascalCase` for class names.
	- File names should be lowercase, use underscores if needed.
	- Follow [PEP8 for Python](https://peps.python.org/pep-0008/).
	- Write clear comments and docstrings for important functions/classes.
	- Do not hardcode values; prefer using configuration variables.
	- Code must be readable, maintainable, and prioritize clean code.

**Goal:** Have a trained model saved in MLflow.

---

### 1.1 Environment Setup

- [ ] Install Python (3.9, 3.10, or 3.11).
- [ ] Install necessary libraries: `tensorflow`, `mlflow`, `flask`, `numpy`, `matplotlib`.
- [ ] Create project directory following the standard structure (see end of file).

---

### 1.2 Develop Training & Experiment Code (Crucial)

- [ ] Write `train.py` to load MNIST data.
- [ ] Build `train_model` function using MLflow (`mlflow.start_run()`).
- [ ] Execute 3 Runs for comparison:
	- **Run 1 (Baseline):** Basic CNN (1 Conv2D layer, 1 Dense layer), low epochs.  
		_Reason: Establish a baseline for comparison._
	- **Run 2 (Tuning Architecture):** Add Dropout layer (to prevent overfitting) and increase the number of filters.  
		_Reason: Verify if a more complex model learns better._
	- **Run 3 (Tuning Hyperparameters):** Keep Run 2 architecture, change `learning_rate` or `batch_size`.  
		_Reason: Optimize the model's convergence speed._

---

### 1.3 Evaluate & Register Model

- [ ] Open MLflow UI ([http://127.0.0.1:5000](http://127.0.0.1:5000)) to view Loss/Accuracy comparison charts.
- [ ] Select the Run with the best results.
- [ ] Register that model to the Model Registry with the name: `Mnist_Best_Model`, and tag it as Production.

---

## PHASE 2: BUILD WEB APP (3 - 4 Hours)

**Goal:** Functional Web App where users can draw numbers and get correct predictions.

---

### 2.1 Backend (Flask)

- [ ] Create `app.py`.
- [ ] Write `load_model` function: Load model from MLflow (or from the saved artifact file of the best Run).
- [ ] Write `/predict` API: Receive image from user → Preprocessing (Reshape 28x28, Grayscale) → Predict → Return result.

---

### 2.2 Frontend (HTML/JS)

- [ ] Create `templates/index.html`.
- [ ] Create a canvas (drawing area) using JavaScript for mouse drawing.
- [ ] "Clear" button to erase the drawing.
- [ ] "Predict" button to send canvas data to the Flask server.

---

### 2.3 Local Testing

- [ ] Run `python app.py`.
- [ ] Draw numbers 3, 5, 7 to test prediction accuracy.

---

## PHASE 3: BONUS CI/CD & DOCKER (2 - 3 Hours)

**Goal:** Automate packaging.

---

### 3.1 Dockerization

- [ ] Write `Dockerfile`:
	- Base image: `python:3.11-slim` (or `3.9-slim`).
	- Copy `requirements.txt` and install.
	- Copy project code.
	- Command: `CMD ["python", "app.py"]`.
- [ ] Test `docker build` and `docker run` locally to ensure the image works.

---

### 3.2 GitHub Actions CI/CD (Replacing GitLab)

- [ ] Create a Docker Hub account and a Repository named `mlops-mnist`.
- [ ] Create a GitHub Repository named `MLOps`.
- [ ] Push all code to GitHub.
- [ ] Configure Secrets on GitHub (`Settings -> Secrets -> Actions`):
	- `DOCKER_USERNAME`
	- `DOCKER_PASSWORD`
- [ ] Create Workflow file `.github/workflows/docker-image.yml`:
	- Trigger: push to main branch.
	- Jobs: Login Docker Hub → Build Image → Push Image.

---

## PHASE 4: SUMMARY & REPORT (2 Hours)

**Goal:** Finalize submission materials.

---

### 4.1 Record Video

- [ ] Screen recording:
	- Open MLflow UI showing experiments.
	- Open Actions tab on GitHub showing green Workflow (Success).
	- Open Docker Hub showing the recently pushed image.
	- Web app demo: Draw and predict.

---

### 4.2 Write Word Report

- [ ] Take screenshots of each step above.
- [ ] Clearly note reasons for parameter tuning (from Phase 1).
- [ ] Paste GitHub Repository link and Video link.

---

## PROJECT DIRECTORY STRUCTURE (SUGGESTED)

