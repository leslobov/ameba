#!/bin/bash

# Ameba Game Stop Script
# This script stops both the backend API server and frontend development server

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

# Function to kill process on port
kill_port() {
    local port=$1
    local service_name=$2
    local pids=$(lsof -ti ":$port" 2>/dev/null)
    
    if [ -n "$pids" ]; then
        print_status "Stopping $service_name on port $port..."
        echo "$pids" | xargs kill -TERM 2>/dev/null || true
        
        # Wait a moment for graceful shutdown
        sleep 2
        
        # Force kill if still running
        local remaining_pids=$(lsof -ti ":$port" 2>/dev/null)
        if [ -n "$remaining_pids" ]; then
            print_warning "Force killing $service_name..."
            echo "$remaining_pids" | xargs kill -9 2>/dev/null || true
        fi
        
        print_success "$service_name stopped"
    else
        print_status "$service_name not running on port $port"
    fi
}

print_status "🛑 Stopping Ameba Game Services..."
echo "================================="

# Stop frontend development server (Angular)
kill_port 4200 "Frontend Development Server"

# Stop backend API server (FastAPI)
kill_port 8000 "Backend API Server"

# Also kill any node processes that might be running our frontend
print_status "Cleaning up any remaining Node.js processes..."
pkill -f "ng serve" 2>/dev/null || true
pkill -f "npm start" 2>/dev/null || true

# Kill any Python processes running our API
print_status "Cleaning up any remaining Python API processes..."
pkill -f "python3 main.py" 2>/dev/null || true
pkill -f "python main.py" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "fastapi" 2>/dev/null || true

# Also kill any processes in the api directory specifically
pkill -f "api/main.py" 2>/dev/null || true

print_success "✅ All Ameba Game services have been stopped"
echo ""
print_status "To start the services again, run: ./start.sh"