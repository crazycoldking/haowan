#!/bin/bash
# Quick start script for GitHub Trending Projects

set -e

echo "🚀 GitHub Trending Projects - Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ Error: pip is not installed"
    exit 1
fi

echo "✓ pip found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1 || pip3 install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"

# Run data collection
echo ""
echo "🔍 Collecting GitHub trending projects..."
cd src
python3 main.py || python main.py
cd ..

echo ""
echo "✅ Data collection complete!"
echo ""
echo "📊 Data saved to:"
echo "   - data/latest.json (latest data)"
echo "   - data/daily/$(date +%Y-%m-%d).json (today's archive)"
echo "   - data/history.json (historical index)"
echo ""
echo "🌐 To view the web interface:"
echo "   python3 -m http.server 8080"
echo "   Then open http://localhost:8080/web/index.html"
echo ""
