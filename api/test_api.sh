#!/bin/bash

# Test script for Ameba API
echo "🧪 Testing Ameba API endpoints..."

API_BASE="http://127.0.0.1:8000"

# Function to test an endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local expected_status=$3
    
    echo -n "Testing $method $endpoint... "
    
    if command -v curl &> /dev/null; then
        response=$(curl -s -w "%{http_code}" -X $method "$API_BASE$endpoint")
        status_code="${response: -3}"
        
        if [ "$status_code" = "$expected_status" ]; then
            echo "✅ PASS ($status_code)"
        else
            echo "❌ FAIL ($status_code, expected $expected_status)"
        fi
    else
        echo "❌ curl not available"
    fi
}

# Check if server is running
echo "🔍 Checking if API server is running on $API_BASE..."
if curl -s --connect-timeout 3 "$API_BASE/health" > /dev/null; then
    echo "✅ Server is running"
    
    # Test endpoints
    echo ""
    echo "🧪 Running API tests..."
    test_endpoint "GET" "/" "200"
    test_endpoint "GET" "/health" "200"
    test_endpoint "GET" "/api/config" "200"
    test_endpoint "GET" "/api/config/play_desk" "200"
    test_endpoint "GET" "/api/config/ameba" "200"
    test_endpoint "GET" "/api/config/neural_network" "200"
    
    echo ""
    echo "📋 API Response Sample:"
    echo "GET /api/config:"
    curl -s "$API_BASE/api/config" | python3 -m json.tool 2>/dev/null || curl -s "$API_BASE/api/config"
    
else
    echo "❌ Server is not running"
    echo ""
    echo "🚀 To start the server:"
    echo "   cd /home/les/projects/ai/ameba/api"
    echo "   source ../.venv/bin/activate"
    echo "   python main.py"
fi