# 🚀 Getting Started - MLOps MNIST Project

**Welcome!** This guide will get you up and running in 5 minutes.

---

## ⚡ Super Quick Start (Automated)

If you want to run everything automatically:

### Mac/Linux:
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run complete pipeline
./run_pipeline.sh
```

### Windows:
```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Run complete pipeline
run_pipeline.bat
```

This will automatically:
- ✅ Verify your environment
- ✅ Train all 3 models
- ✅ Register the best model
- ✅ Show you next steps

**Estimated time: 15-20 minutes**

---

## 🎯 Manual Step-by-Step

If you prefer to run each step manually:

### Step 1: Setup Environment (2 minutes)

```bash
# Create virtual environment (if not already done)
python3.11 -m venv venv

# Activate it
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python scripts/test_setup.py
```

### Step 2: Train Models (10-15 minutes)

```bash
# Run training script
python src/train.py
```

This will train 3 different models and log everything to MLflow.

**☕ Grab a coffee while it trains!**

### Step 3: View Results (2 minutes)

```bash
# Start MLflow UI
mlflow ui
```

Then open your browser to: **http://127.0.0.1:5000**

You'll see:
- 📊 All 3 experiment runs
- 📈 Accuracy and loss comparisons
- 📉 Training curves
- 🎯 Metrics for each run

### Step 4: Register Best Model (1 minute)

**Option A - Automatic (Recommended):**
```bash
# In a new terminal (keep MLflow UI running)
python scripts/register_model.py
```

**Option B - Manual:**
1. In MLflow UI, click on the run with highest accuracy
2. Click "Register Model"
3. Name: `Mnist_Best_Model`
4. Stage: `Production`

### Step 5: Run Web App (1 minute)

```bash
# Stop MLflow UI first (Ctrl+C)

# Run Flask app
python src/app.py
```

Open browser to: **http://127.0.0.1:5000**

**Try it out:**
1. ✏️ Draw a digit (try 3, 5, or 7)
2. 🔮 Click "Predict"
3. 🎯 See the AI's prediction!
4. 🗑️ Click "Clear" to try again

---

## 🐳 Bonus: Docker (Optional)

If you want to run in Docker:

```bash
# Build image
docker build -t mlops-mnist .

# Run container
docker run -p 5000:5000 mlops-mnist
```

Open browser to: **http://127.0.0.1:5000**

---

## 📊 What to Expect

### Training Results
- **Run 1 (Baseline)**: ~98.0% accuracy - Simple model
- **Run 2 (Improved)**: ~98.5% accuracy - Better architecture
- **Run 3 (Optimized)**: ~99.0% accuracy - Best hyperparameters

### Web App Behavior
- Draw digits clearly and centered for best results
- The AI was trained on MNIST (handwritten digits)
- Predictions are usually very accurate (99%+)
- You'll see probability bars for all 10 digits (0-9)

---

## 🆘 Troubleshooting

### "Port 5000 already in use"
```bash
# Kill the process
lsof -ti:5000 | xargs kill -9

# Or use different port
mlflow ui --port 5001
```

### "Module not found" error
```bash
# Make sure you're in virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Model not found" in web app
```bash
# Train models first
python src/train.py

# Register model
python scripts/register_model.py
```

### Docker build fails
```bash
# Clear Docker cache
docker system prune -a

# Rebuild
docker build --no-cache -t mlops-mnist .
```

---

## 📚 More Help

- **Detailed Guide**: See `SETUP_GUIDE.md`
- **Full Documentation**: See `README.md`
- **Command Reference**: See `COMMANDS.md`
- **Project Summary**: See `PROJECT_SUMMARY.md`

---

## 🎯 Quick Commands Reference

```bash
# View quick start options
python scripts/quick_start.py

# Check environment
python scripts/test_setup.py

# Train models
python src/train.py

# View experiments
mlflow ui

# Register model
python scripts/register_model.py

# Run web app
python src/app.py

# Run complete pipeline
./run_pipeline.sh       # Mac/Linux
run_pipeline.bat        # Windows
```

---

## ✅ Checklist

Before moving to next step, make sure:

- [ ] Virtual environment activated (you should see `(venv)` in terminal)
- [ ] All packages installed (`pip list` shows tensorflow, mlflow, flask)
- [ ] Python 3.9+ (`python --version`)

After training:
- [ ] MLflow UI shows 3 runs
- [ ] All runs completed successfully
- [ ] Best model has ~99% accuracy

After model registration:
- [ ] Model appears in MLflow Models tab
- [ ] Model stage is "Production"

After running web app:
- [ ] Can access http://127.0.0.1:5000
- [ ] Can draw on canvas
- [ ] Predictions work correctly
- [ ] Can clear and redraw

---

## 🎉 Success!

If you can:
1. ✅ Draw a digit
2. ✅ Get correct prediction
3. ✅ See confidence scores

**Congratulations! Your MLOps pipeline is working! 🎊**

---

## 🔜 Next Steps

1. **Try all digits (0-9)** - Test the model's accuracy
2. **View MLflow UI** - Explore experiment tracking
3. **Modify code** - Try changing model architecture
4. **Deploy to cloud** - Use Docker image for deployment
5. **Set up CI/CD** - Push to GitHub and enable Actions

---

## 💡 Pro Tips

- Keep MLflow UI open while experimenting to see runs in real-time
- Use `Ctrl+C` to stop servers (MLflow UI, Flask app)
- Try drawing digits in different styles (bold, thin, angled)
- Check model probabilities to understand confidence
- Use Docker for consistent deployment environments

---

**Ready to start? Run:** `python scripts/quick_start.py`

**Questions?** Check the troubleshooting section above or see `README.md`

---

**Happy Learning! 🚀**
