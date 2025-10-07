#!/bin/bash

# Ameba Game Backend Only Start Script
# This script only starts the backend API server (no frontend)

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "🐍 Starting Backend API Server Only..."
echo "======================================"

# Get the script directory (project root)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# Check if API directory exists
API_DIR="$PROJECT_ROOT/api"
if [ ! -d "$API_DIR" ]; then
    print_error "API directory not found: $API_DIR"
    exit 1
fi

# Check if API start script exists
if [ ! -f "$API_DIR/start.sh" ]; then
    print_error "API start script not found: $API_DIR/start.sh"
    exit 1
fi

print_status "Using API directory: $API_DIR"
print_success "Backend will be available at: http://localhost:8000"
print_success "API Documentation: http://localhost:8000/docs"
echo ""

# Navigate to API directory and run the start script
cd "$API_DIR"
./start.sh