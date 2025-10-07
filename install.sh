#!/bin/bash

# Ameba Game Installation Script
# This script installs all dependencies for both backend (Python) and frontend (Node.js)

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

print_status "🚀 Starting Ameba Game Installation..."
echo "=================================="

# Get the script directory (project root)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

print_status "📁 Project root: $PROJECT_ROOT"

# Check system requirements
print_status "🔍 Checking system requirements..."

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 is required but not installed. Please install Python 3.8+"
    exit 1
fi

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_success "Node.js found: $NODE_VERSION"
else
    print_error "Node.js is required but not installed. Please install Node.js 16+"
    exit 1
fi

# Check npm
if command_exists npm; then
    NPM_VERSION=$(npm --version)
    print_success "npm found: $NPM_VERSION"
else
    print_error "npm is required but not installed. Please install npm"
    exit 1
fi

# Check pip
if command_exists pip3; then
    PIP_VERSION=$(pip3 --version 2>&1 | cut -d' ' -f2)
    print_success "pip found: $PIP_VERSION"
else
    print_error "pip3 is required but not installed. Please install pip3"
    exit 1
fi

echo ""
print_status "🐍 Setting up Python backend environment..."
echo "===========================================" 

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv .venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python requirements
if [ -f "requirements.txt" ]; then
    print_status "Installing Python dependencies from requirements.txt..."
    pip install -r requirements.txt
    print_success "Python dependencies installed"
else
    print_warning "requirements.txt not found, skipping Python dependencies"
fi

# Install API specific requirements if they exist
if [ -f "api/requirements.txt" ]; then
    print_status "Installing API specific dependencies..."
    pip install -r api/requirements.txt
    print_success "API dependencies installed"
fi

echo ""
print_status "📦 Setting up Node.js frontend environment..."
echo "============================================="

# Navigate to frontend directory
FRONTEND_DIR="$PROJECT_ROOT/frontend/ameba-app"

if [ -d "$FRONTEND_DIR" ]; then
    cd "$FRONTEND_DIR"
    
    # Check if package.json exists
    if [ -f "package.json" ]; then
        print_status "Installing Node.js dependencies..."
        
        # Clean install
        if [ -d "node_modules" ]; then
            print_status "Removing existing node_modules..."
            rm -rf node_modules
        fi
        
        if [ -f "package-lock.json" ]; then
            print_status "Using npm ci for clean install..."
            npm ci
        else
            print_status "Using npm install..."
            npm install
        fi
        
        print_success "Node.js dependencies installed"
        
        # Build the frontend
        print_status "Building Angular frontend..."
        npm run build
        print_success "Frontend built successfully"
        
    else
        print_error "package.json not found in $FRONTEND_DIR"
        exit 1
    fi
else
    print_error "Frontend directory not found: $FRONTEND_DIR"
    exit 1
fi

# Return to project root
cd "$PROJECT_ROOT"

echo ""
print_status "🔧 Setting up project configuration..."
echo "======================================"

# Check if config.json exists
if [ -f "config.json" ]; then
    print_success "Configuration file found: config.json"
else
    print_warning "config.json not found. You may need to create it manually."
fi

# Make scripts executable
print_status "Making scripts executable..."
if [ -f "api/start.sh" ]; then
    chmod +x api/start.sh
    print_success "api/start.sh made executable"
fi

if [ -f "api/setup.sh" ]; then
    chmod +x api/setup.sh
    print_success "api/setup.sh made executable"
fi

echo ""
print_success "✅ Installation completed successfully!"
echo "======================================"
echo ""
print_status "🚀 Quick Start Guide:"
echo ""
echo "1. Start the backend API server:"
echo "   cd api && ./start.sh"
echo "   or"
echo "   cd api && python3 main.py"
echo ""
echo "2. Start the frontend development server:"
echo "   cd frontend/ameba-app && npm start"
echo ""
echo "3. Open your browser and navigate to:"
echo "   Frontend: http://localhost:4200"
echo "   API Docs: http://localhost:8000/docs"
echo ""
print_status "📚 Available commands:"
echo "   Backend API: cd api && python3 main.py"
echo "   Frontend Dev: cd frontend/ameba-app && npm start"
echo "   Frontend Build: cd frontend/ameba-app && npm run build"
echo "   Run Tests: python3 -m pytest tests/"
echo ""
print_success "Happy coding! 🎮"