#!/bin/bash
# Enterprise MLOps Setup Script

set -e  # Exit on error

echo "=========================================="
echo "Enterprise MLOps MNIST Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "\n${YELLOW}Checking Python version...${NC}"
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD=python3.12
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD=python3.11
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    echo -e "${RED}Error: Python 3.11+ is required${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version)
echo -e "${GREEN}Found: $PYTHON_VERSION${NC}"

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
$PYTHON_CMD -m venv .venv
echo -e "${GREEN}Virtual environment created${NC}"

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "\n${YELLOW}Installing production dependencies...${NC}"
pip install -r requirements.txt

echo -e "\n${YELLOW}Installing development dependencies...${NC}"
pip install -r requirements-dev.txt

# Setup environment file
if [ ! -f .env ]; then
    echo -e "\n${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}.env file created. Please update with your configuration.${NC}"
else
    echo -e "\n${GREEN}.env file already exists${NC}"
fi

# Setup pre-commit hooks
echo -e "\n${YELLOW}Installing pre-commit hooks...${NC}"
pre-commit install
echo -e "${GREEN}Pre-commit hooks installed${NC}"

# Create necessary directories
echo -e "\n${YELLOW}Creating project directories...${NC}"
mkdir -p mlruns mlartifacts logs

# Verify installation
echo -e "\n${YELLOW}Verifying installation...${NC}"
python -c "import tensorflow; import mlflow; import fastapi; print('✓ All core packages installed')"

echo -e "\n${GREEN}=========================================="
echo "Setup completed successfully!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Configure .env file with your settings"
echo "  3. Train models: python src/training/train.py"
echo "  4. Register model: python scripts/register_model.py"
echo "  5. Start API: python src/api/main.py"
echo ""
echo "Or use Docker Compose:"
echo "  docker-compose up -d"
echo ""
echo "For more information, see QUICKSTART.md"
