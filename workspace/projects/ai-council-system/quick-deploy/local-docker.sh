#!/bin/bash
# AI Council System - Local Docker Quick Deploy
# For local development and testing

set -e

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=================================================="
echo "AI Council System - Local Docker Deployment"
echo "=================================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker not found. Please install Docker first:${NC}"
    echo "  https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env and add your API keys:"
    echo "   nano .env"
    echo ""
    echo "Required:"
    echo "  - ANTHROPIC_API_KEY=your_key_here"
    echo "  - OPENAI_API_KEY=your_key_here"
    echo ""
    read -p "Press Enter when ready to continue..."
fi

echo -e "${GREEN}Building Docker images...${NC}"
docker-compose -f docker/docker-compose.yml build

echo -e "${GREEN}Starting services...${NC}"
docker-compose -f docker/docker-compose.yml up -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

# Check health
if curl -f http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Services are healthy${NC}"
else
    echo -e "${YELLOW}⚠ Services starting... (may take a minute)${NC}"
fi

echo ""
echo "=================================================="
echo -e "${GREEN}AI Council System is Running!${NC}"
echo "=================================================="
echo ""
echo "🌐 Access Points:"
echo "   Dashboard:  http://localhost:8000/dashboard"
echo "   API Docs:   http://localhost:8000/docs"
echo "   Health:     http://localhost:8000/api/v1/health"
echo ""
echo "🔧 Management:"
echo "   View logs:     docker-compose -f docker/docker-compose.yml logs -f"
echo "   Stop:          docker-compose -f docker/docker-compose.yml down"
echo "   Restart:       docker-compose -f docker/docker-compose.yml restart"
echo ""
echo "🎮 Quick Commands:"
echo "   Run demo:      ./ai-council demo --mock"
echo "   Start debate:  ./ai-council debate start \"Your topic here\""
echo "   Check status:  ./ai-council health"
echo ""
echo "=================================================="
