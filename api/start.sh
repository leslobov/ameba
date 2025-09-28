#!/bin/bash

# Start the Ameba API server
echo "🚀 Starting Ameba API server..."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Using virtual environment: $VIRTUAL_ENV"
else
    echo "⚠️  Activating virtual environment..."
    cd ..
    source .venv/bin/activate
    cd api
fi

# Start the server
echo "🌐 Starting server at http://127.0.0.1:8000"
echo "📚 API documentation at http://127.0.0.1:8000/docs"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python main.py