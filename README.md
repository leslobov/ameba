# 🎮 Ameba Game - AI Simulation Project

An interactive AI simulation game where amebas move around a board using neural networks to find food and survive. The project features a FastAPI backend with a neural network simulation engine and an Angular frontend for visualization and control.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Stopping the Application](#-stopping-the-application)
- [Development](#-development)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)

## 🌟 Features

- **AI-Powered Amebas**: Neural network-driven entities that learn to find food
- **Real-time Simulation**: Live game board with movement animations
- **Interactive Controls**: Manual stepping, auto-play, and simulation modes
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Modern Frontend**: Angular application with Material Design
- **Configurable Parameters**: Adjustable game settings and neural network parameters
- **Real-time Visualization**: Animated game board with energy indicators

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/REST    ┌──────────────────┐
│  Angular Frontend │ ◄─────────────► │  FastAPI Backend │
│  (Port 4200)     │                 │  (Port 8000)     │
└─────────────────┘                 └──────────────────┘
        │                                    │
        ▼                                    ▼
┌─────────────────┐                 ┌──────────────────┐
│   Game Board    │                 │  Neural Network  │
│   Visualization │                 │     Engine       │
└─────────────────┘                 └──────────────────┘
```

## 📦 Prerequisites

Before running the Ameba Game, ensure you have the following installed:

- **Python 3.8+** (recommended: Python 3.10+)
- **Node.js 16+** (recommended: Node.js 18+)
- **npm** (comes with Node.js)
- **Git** (for cloning the repository)

### System Requirements

- **Operating System**: Linux, macOS, or Windows with WSL
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space for dependencies

## 🚀 Quick Start

Get the Ameba Game running in 3 simple steps:

```bash
# 1. Clone the repository
git clone <repository-url>
cd ameba

# 2. Install all dependencies
./install.sh

# 3. Start the application
./start.sh
```

That's it! The game will be available at:
- **Frontend**: http://localhost:4200
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🔧 Installation

### Automatic Installation (Recommended)

The installation script handles everything automatically:

```bash
./install.sh
```

**What it does:**
- ✅ Creates Python virtual environment
- ✅ Installs all Python dependencies
- ✅ Installs Node.js dependencies
- ✅ Builds the Angular frontend
- ✅ Sets up project configuration
- ✅ Makes scripts executable

### Manual Installation

If you prefer manual setup:

#### Backend Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend/ameba-app

# Install Node.js dependencies
npm install

# Build the application
npm run build

# Run the application in the development mode (port 4200)
npm start
```

## 🎯 Running the Application

### Option 1: Full Stack (Recommended)

Start both frontend and backend together:

```bash
./start.sh
```

**Behavior:**
- 🌐 **Frontend**: Runs as daemon (background process)
- 🐍 **Backend**: Runs with console logging (foreground)
- 📝 **Logs**: Frontend logs saved to `logs/frontend.log`

**Services Available:**
- Frontend: http://localhost:4200
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Option 2: Backend Only

Start just the API server:

```bash
./start-backend.sh
```

**Use Case**: When you only need the API for development or testing.

### Option 3: Individual Services

Start services separately:

```bash
# Backend only
cd api && ./start.sh

# Frontend only (in another terminal)
cd frontend/ameba-app && npm start
```

## 🛑 Stopping the Application

### Stop All Services

```bash
./stop.sh
```

**What it does:**
- 🛑 Stops frontend development server (port 4200)
- 🛑 Stops backend API server (port 8000)
- 🧹 Cleans up all related processes
- 🔄 Frees up ports for restart

### Manual Stop

If the stop script doesn't work:

```bash
# Kill processes by port
lsof -ti :4200 | xargs kill -9  # Frontend
lsof -ti :8000 | xargs kill -9  # Backend

# Or kill by process name
pkill -f "npm start"
pkill -f "python3 main.py"
```

### Stop Individual Services

```bash
# Stop frontend only
pkill -f "npm start"

# Stop backend only
pkill -f "python3 main.py"
```

## 🔨 Development

### Development Workflow

1. **Start Development Environment**:
   ```bash
   ./start.sh
   ```

2. **Make Changes**:
   - Backend: Edit files in `api/` or `core/`
   - Frontend: Edit files in `frontend/ameba-app/src/`

3. **Testing**:
   ```bash
   # Run Python tests
   python3 -m pytest tests/
   
   # Test API endpoints
   curl http://localhost:8000/health
   ```

4. **View Logs**:
   ```bash
   # Frontend logs (when running as daemon)
   tail -f logs/frontend.log
   
   # Backend logs (visible in console)
   # Already displayed when running ./start.sh
   ```

### Hot Reloading

- **Frontend**: Automatic reload on file changes (Angular dev server)
- **Backend**: Automatic reload on file changes (FastAPI with `--reload`)

### Useful Development Commands

```bash
# Install new Python package
source .venv/bin/activate
pip install <package-name>
pip freeze > requirements.txt

# Install new Node.js package
cd frontend/ameba-app
npm install <package-name>

# Run linting
flake8 core/ api/
cd frontend/ameba-app && npm run lint

# Run type checking
mypy core/ api/
```

## 📚 API Documentation

The API documentation is automatically generated and available at:

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/config` | GET | Get game configuration |
| `/api/movement/move` | POST | Move amebas |
| `/api/movement/simulate` | POST | Run simulation |
| `/api/movement/status` | GET | Get movement status |
| `/api/movement/state` | GET | Get current game state |

### Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Get configuration
curl http://localhost:8000/api/config

# Get current game state
curl http://localhost:8000/api/movement/state
```

## ⚙️ Configuration

### Game Configuration

Edit `config.json` to modify game parameters:

```json
{
  "play_desk": {
    "rows": 12,
    "columns": 12,
    "total_energy": 600,
    "energy_per_food": 50
  },
  "ameba": {
    "initial_energy": 100,
    "visible_rows": 3,
    "visible_columns": 3
  },
  "neural_network": {
    "initial_hidden_layers": 1,
    "initial_neurons_on_layer": 10
  }
}
```

### Environment Variables

Create `.env` file for environment-specific settings:

```bash
# API Configuration
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=true

# Frontend Configuration
FRONTEND_PORT=4200
```

## 📁 Project Structure

```
ameba/
├── 📜 README.md              # This file
├── 🚀 install.sh             # Installation script
├── ▶️  start.sh              # Start all services
├── ⏹️  start-backend.sh      # Start backend only
├── 🛑 stop.sh               # Stop all services
├── ⚙️  config.json           # Game configuration
├── 📄 requirements.txt       # Python dependencies
│
├── 🐍 api/                   # Backend API
│   ├── main.py              # FastAPI application
│   ├── start.sh             # Backend start script
│   └── movement/            # Movement endpoints
│
├── 🧠 core/                  # Game engine
│   ├── game.py              # Main game class
│   ├── ameba.py             # Ameba entity
│   ├── neural_network/      # AI engine
│   └── config_classes/      # Configuration models
│
├── 🌐 frontend/             # Frontend application
│   └── ameba-app/           # Angular app
│       ├── src/             # Source code
│       ├── package.json     # Node.js dependencies
│       └── angular.json     # Angular configuration
│
├── 🧪 tests/                # Test files
├── 📊 logs/                 # Log files
└── 🎨 uml/                  # UML diagrams
```

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Error: Port 4200/8000 is already in use
./stop.sh  # Stop all services
./start.sh # Restart
```

#### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf .venv
./install.sh
```

#### Frontend Build Errors
```bash
# Clear Node.js cache and reinstall
cd frontend/ameba-app
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### Python Dependencies Issues
```bash
# Update pip and reinstall
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Checking Service Status

```bash
# Check if services are running
curl http://localhost:8000/health  # Backend
curl http://localhost:4200         # Frontend

# Check ports
lsof -i :8000  # Backend port
lsof -i :4200  # Frontend port
```

### Log Files

```bash
# Backend logs (when running ./start.sh)
# Visible in terminal

# Frontend logs (when running as daemon)
tail -f logs/frontend.log

# System logs
journalctl -f  # Linux
tail -f /var/log/system.log  # macOS
```

### Performance Issues

```bash
# Check system resources
htop           # Process monitor
df -h          # Disk space
free -h        # Memory usage
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `python3 -m pytest tests/`
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review logs in `logs/frontend.log`
3. Check API documentation at http://localhost:8000/docs
4. Open an issue on GitHub

---

**Happy Gaming! 🎮**