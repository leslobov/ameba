#!/bin/bash

# Setup script for Ameba API server
echo "🚀 Setting up Ameba API server..."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected. Activating .venv..."
    cd ..
    if [ ! -d ".venv" ]; then
        echo "❌ .venv directory not found. Please create a virtual environment first."
        echo "Run: python -m venv .venv"
        exit 1
    fi
    source .venv/bin/activate
    cd api
fi

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "🎯 To start the API server:"
echo "   python main.py"
echo ""
echo "🌐 API will be available at:"
echo "   http://127.0.0.1:8000"
echo "   http://127.0.0.1:8000/docs (Swagger UI)"
echo ""
echo "🔗 Available endpoints:"
echo "   GET  /api/config       - Get full configuration"
echo "   PUT  /api/config       - Update full configuration"
echo "   GET  /api/config/{section} - Get specific section"
echo "   PUT  /api/config/{section} - Update specific section"
echo "   POST /api/config/reset - Reset to defaults"