#!/bin/bash
# AI Council System - Codespaces Setup Script

set -e

echo "🚀 Setting up AI Council System in GitHub Codespaces..."
echo ""

# Update package lists
echo "📦 Updating package lists..."
sudo apt-get update -qq

# Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apt-get install -y -qq \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    postgresql-client \
    redis-tools \
    > /dev/null

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p recordings
mkdir -p voice_cache
mkdir -p avatar_cache
mkdir -p background_cache
mkdir -p logs
mkdir -p data

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys!"
    echo "   - ANTHROPIC_API_KEY"
    echo "   - OPENAI_API_KEY"
    echo "   - ELEVEN_API_KEY (optional)"
    echo "   - Streaming keys (optional)"
    echo ""
fi

# Make scripts executable
chmod +x quick-start.sh 2>/dev/null || true
chmod +x run-demo.sh 2>/dev/null || true

echo "✅ Setup complete!"
echo ""
echo "🎯 Quick Start Commands:"
echo "   ./quick-start.sh         - Run interactive demo"
echo "   python examples/phase5_complete_demo.py - Full automation demo"
echo "   docker-compose up -d     - Start all services"
echo ""
echo "📚 Documentation:"
echo "   README.md                - Project overview"
echo "   deployment/README.md     - Production deployment guide"
echo ""
echo "🔑 Don't forget to configure your .env file with API keys!"
