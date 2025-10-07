#!/bin/bash

# Ameba Game Start Script
# This script starts both the backend API server and frontend development server
# Frontend runs as daemon, backend runs with console logging

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

print_daemon() {
    echo -e "${CYAN}[DAEMON]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if port is in use
port_in_use() {
    lsof -i ":$1" >/dev/null 2>&1
}

# Function to kill process on port
kill_port() {
    local port=$1
    local pids=$(lsof -ti ":$port" 2>/dev/null)
    if [ -n "$pids" ]; then
        echo "$pids" | xargs kill -9 2>/dev/null || true
        print_status "Killed processes on port $port"
    fi
}

# Cleanup function
cleanup() {
    print_status "🛑 Shutting down services..."
    
    # Kill frontend process if running
    if [ -n "$FRONTEND_PID" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
        print_daemon "Stopping frontend development server (PID: $FRONTEND_PID)..."
        kill "$FRONTEND_PID" 2>/dev/null || true
        wait "$FRONTEND_PID" 2>/dev/null || true
    fi
    
    # Kill any remaining processes on our ports
    kill_port 4200  # Angular dev server
    kill_port 8000  # FastAPI server
    
    print_success "✅ Services stopped"
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM EXIT

print_status "🚀 Starting Ameba Game Services..."
echo "=================================="

# Get the script directory (project root)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

print_status "📁 Project root: $PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    print_error "Virtual environment not found. Please run ./install.sh first"
    exit 1
fi

# Check if frontend directory exists
FRONTEND_DIR="$PROJECT_ROOT/frontend/ameba-app"
if [ ! -d "$FRONTEND_DIR" ]; then
    print_error "Frontend directory not found: $FRONTEND_DIR"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    print_error "Frontend dependencies not installed. Please run ./install.sh first"
    exit 1
fi

# Kill any existing processes on our ports
print_status "🧹 Cleaning up existing processes..."
kill_port 4200
kill_port 8000

echo ""
print_daemon "🌐 Starting Frontend Development Server (Daemon)..."
echo "================================================="

# Start frontend as daemon
cd "$FRONTEND_DIR"

# Create log directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/logs"

# Start npm start in background and capture PID
npm start > "$PROJECT_ROOT/logs/frontend.log" 2>&1 &
FRONTEND_PID=$!

print_daemon "Frontend server starting in background (PID: $FRONTEND_PID)"
print_daemon "Frontend logs: $PROJECT_ROOT/logs/frontend.log"

# Wait a moment for frontend to start
print_status "⏳ Waiting for frontend to initialize..."
sleep 5

# Check if frontend is still running
if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
    print_error "Frontend failed to start. Check logs:"
    tail -n 20 "$PROJECT_ROOT/logs/frontend.log"
    exit 1
fi

print_success "Frontend development server is running in background"
print_daemon "Frontend URL: http://localhost:4200"

echo ""
print_status "🐍 Starting Backend API Server (Console Logging)..."
echo "===================================================="

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

# Make sure API start script is executable
chmod +x "$API_DIR/start.sh"

# Start backend using the API start script
print_status "🚀 Starting Backend API server through api/start.sh..."
print_status "📚 API Documentation: http://localhost:8000/docs"
print_status "🔗 Health Check: http://localhost:8000/health"
echo ""
print_status "==============================================="
print_status "🎮 AMEBA GAME IS RUNNING!"
print_status "==============================================="
print_status "Frontend: http://localhost:4200"
print_status "API: http://localhost:8000"
print_status "API Docs: http://localhost:8000/docs"
print_status "==============================================="
print_warning "Press Ctrl+C to stop all services"
echo ""

# Navigate to API directory and run the start script
cd "$API_DIR"
./start.sh