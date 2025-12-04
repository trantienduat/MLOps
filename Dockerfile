# Dockerfile for MLOps MNIST Project
# Base image: Python 3.11 slim
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port 5000 for Flask application
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the Flask application
CMD ["python", "app.py"]
