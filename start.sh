#!/bin/bash

# Startup Revenue Insights Tracker - Start Script
echo "🚀 Starting Startup Revenue Insights Tracker..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
uv pip install -r requirements.txt

# Install additional dependencies for the dashboard
uv pip install streamlit plotly

echo "✅ Environment setup complete!"

# Start the dashboard
echo "🌐 Starting Streamlit dashboard..."
echo "Dashboard will be available at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"

streamlit run dashboard.py --server.port 8501