#!/bin/bash

# MLOps MNIST Project - Complete Pipeline Runner
# This script runs the entire MLOps pipeline from start to finish

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Main execution
main() {
    print_header "MLOps MNIST - Complete Pipeline"
    
    # Step 1: Check environment
    print_header "Step 1: Checking Environment"
    if python test_setup.py; then
        print_success "Environment check passed"
    else
        print_error "Environment check failed"
        exit 1
    fi
    
    # Step 2: Run training
    print_header "Step 2: Training Models (This may take 10-15 minutes)"
    if [ -f "train.py" ]; then
        python train.py
        print_success "Training completed"
    else
        print_error "train.py not found"
        exit 1
    fi
    
    # Step 3: Register best model
    print_header "Step 3: Registering Best Model"
    print_warning "Please follow the prompts to register the model"
    python register_model.py
    
    # Step 4: Information
    print_header "Pipeline Complete!"
    echo -e "${GREEN}All steps completed successfully!${NC}\n"
    
    echo "Next steps:"
    echo "1. View experiments:"
    echo -e "   ${YELLOW}mlflow ui${NC}"
    echo -e "   Then open: ${BLUE}http://127.0.0.1:5000${NC}\n"
    
    echo "2. Run web application:"
    echo -e "   ${YELLOW}python app.py${NC}"
    echo -e "   Then open: ${BLUE}http://127.0.0.1:5000${NC}\n"
    
    echo "3. Build Docker image:"
    echo -e "   ${YELLOW}docker build -t mlops-mnist .${NC}\n"
    
    echo "4. Run with Docker:"
    echo -e "   ${YELLOW}docker run -p 5000:5000 mlops-mnist${NC}\n"
}

# Run main function
main
