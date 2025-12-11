#!/bin/bash
# AI Council System - Quick Start Interactive Demo

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║          🤖 AI COUNCIL SYSTEM - QUICK START 🤖            ║"
echo "║                                                            ║"
echo "║          Interactive Multi-AI Debate Platform             ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: .env file not found!${NC}"
    echo ""
    echo "Please create a .env file with your API keys:"
    echo "  cp .env.example .env"
    echo ""
    echo "Then edit .env and add:"
    echo "  - ANTHROPIC_API_KEY=your_key_here"
    echo "  - OPENAI_API_KEY=your_key_here"
    echo ""
    exit 1
fi

# Check for required API keys
source .env
if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${RED}❌ Error: No API keys configured!${NC}"
    echo ""
    echo "Please edit .env and add at least one of:"
    echo "  - ANTHROPIC_API_KEY"
    echo "  - OPENAI_API_KEY"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Configuration loaded${NC}"
echo ""

# Menu
echo -e "${YELLOW}What would you like to do?${NC}"
echo ""
echo "  1) 🎬 Run a Quick Debate Demo (5 AI agents, single topic)"
echo "  2) 🎭 See Avatar System Demo (visual personalities)"
echo "  3) 🎨 See Video Effects Demo (transitions, visualizations)"
echo "  4) 🎙️  See Voice Cloning Demo (unique voices per agent)"
echo "  5) 🌈 See Dynamic Backgrounds Demo (sentiment-reactive)"
echo "  6) 🤖 Run Full Automation Demo (Phase 5 complete)"
echo "  7) 🎪 Run Comprehensive Integration (everything together)"
echo "  8) 🔧 Start Production Services (Docker Compose)"
echo "  9) 📊 View System Status"
echo "  0) ❌ Exit"
echo ""
echo -n "Enter your choice (0-9): "
read choice

echo ""

case $choice in
    1)
        echo -e "${CYAN}🎬 Starting Quick Debate Demo...${NC}"
        echo ""
        python examples/demo_debate.py
        ;;
    2)
        echo -e "${CYAN}🎭 Starting Avatar System Demo...${NC}"
        echo ""
        python examples/avatar_demo.py
        ;;
    3)
        echo -e "${CYAN}🎨 Starting Video Effects Demo...${NC}"
        echo ""
        python examples/effects_demo.py
        ;;
    4)
        echo -e "${CYAN}🎙️  Starting Voice Cloning Demo...${NC}"
        echo ""
        python examples/voice_cloning_demo.py
        ;;
    5)
        echo -e "${CYAN}🌈 Starting Dynamic Backgrounds Demo...${NC}"
        echo ""
        python examples/backgrounds_demo.py
        ;;
    6)
        echo -e "${CYAN}🤖 Starting Full Automation Demo...${NC}"
        echo ""
        python examples/phase5_complete_demo.py
        ;;
    7)
        echo -e "${CYAN}🎪 Starting Comprehensive Integration...${NC}"
        echo ""
        python examples/comprehensive_integration.py
        ;;
    8)
        echo -e "${CYAN}🔧 Starting Production Services...${NC}"
        echo ""
        echo "This will start:"
        echo "  - AI Council Application"
        echo "  - PostgreSQL Database"
        echo "  - Redis Cache"
        echo "  - Nginx Reverse Proxy"
        echo "  - Prometheus Metrics"
        echo "  - Grafana Dashboards"
        echo ""
        echo -n "Continue? (y/n): "
        read confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            docker-compose -f deployment/docker-compose.production.yml up -d
            echo ""
            echo -e "${GREEN}✅ Services started!${NC}"
            echo ""
            echo "Access points:"
            echo "  - API: http://localhost:8000"
            echo "  - Grafana: http://localhost:3000 (admin/admin)"
            echo "  - Prometheus: http://localhost:9090"
            echo ""
            echo "To stop services:"
            echo "  docker-compose -f deployment/docker-compose.production.yml down"
        fi
        ;;
    9)
        echo -e "${CYAN}📊 System Status${NC}"
        echo ""
        echo "Project Structure:"
        echo "  ✅ Core agents & debate engine"
        echo "  ✅ Event ingestion & processing"
        echo "  ✅ Blockchain integration & tokenomics"
        echo "  ✅ Avatar generation & composition"
        echo "  ✅ Video effects & transitions"
        echo "  ✅ Voice cloning & synthesis"
        echo "  ✅ Sentiment-based backgrounds"
        echo "  ✅ Automation & orchestration"
        echo "  ✅ Multi-platform streaming"
        echo "  ✅ Health monitoring & analytics"
        echo "  ✅ Production deployment infrastructure"
        echo ""
        echo "Configuration:"
        if [ ! -z "$ANTHROPIC_API_KEY" ]; then
            echo "  ✅ Anthropic API Key configured"
        else
            echo "  ❌ Anthropic API Key missing"
        fi
        if [ ! -z "$OPENAI_API_KEY" ]; then
            echo "  ✅ OpenAI API Key configured"
        else
            echo "  ❌ OpenAI API Key missing"
        fi
        if [ ! -z "$ELEVEN_API_KEY" ]; then
            echo "  ✅ ElevenLabs API Key configured"
        else
            echo "  ⚠️  ElevenLabs API Key not configured (optional)"
        fi
        echo ""
        echo "Directories:"
        ls -ld recordings voice_cache avatar_cache background_cache logs data 2>/dev/null || echo "  (Creating on first run)"
        ;;
    0)
        echo -e "${YELLOW}👋 Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Invalid choice!${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Demo complete!${NC}"
echo ""
echo "Run ${CYAN}./quick-start.sh${NC} again to try another demo."
