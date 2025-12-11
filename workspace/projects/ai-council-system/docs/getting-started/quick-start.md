# Quick Start Guide

Get your AI Council System up and running in 5 minutes!

## Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** or **Docker**
- **API Keys** for at least one LLM provider:
    - [Anthropic API Key](https://console.anthropic.com/) (recommended)
    - [OpenAI API Key](https://platform.openai.com/api-keys) (alternative)
- **4GB+ RAM** available
- **Git** installed

## Option 1: Docker (Recommended)

The fastest way to get started:

```bash
# 1. Clone the repository
git clone https://github.com/your-org/ai-council-system.git
cd ai-council-system

# 2. Create and configure .env file
cp .env.example .env
nano .env  # Add your API keys

# 3. Start the system
docker-compose -f docker/docker-compose.yml up -d

# 4. Verify it's running
curl http://localhost:8000/api/v1/health

# 5. Run your first debate!
./ai-council debate start "Should AI be regulated?" --agents 5 --rounds 3
```

!!! success "System Ready!"
    Your AI Council System is now running at:

    - **Dashboard**: http://localhost:8000/dashboard
    - **API Docs**: http://localhost:8000/docs
    - **Health**: http://localhost:8000/api/v1/health

## Option 2: Python Installation

For development or customization:

```bash
# 1. Clone repository
git clone https://github.com/your-org/ai-council-system.git
cd ai-council-system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
nano .env  # Add your API keys

# 5. Initialize database
python -c "from core.database import init_db; init_db()"

# 6. Run the system
python -m core.main
```

## Option 3: One-Click Cloud Deploy

Deploy to cloud platforms instantly:

=== "DigitalOcean"

    ```bash
    # Using DigitalOcean CLI
    curl -fsSL https://raw.githubusercontent.com/your-org/ai-council-system/main/quick-deploy/digitalocean-setup.sh | sudo bash
    ```

    Or use the [Deploy Button](../deployment/quick-deploy/digitalocean.md)

=== "Heroku"

    [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/your-org/ai-council-system)

=== "AWS"

    ```bash
    aws cloudformation create-stack \
      --stack-name ai-council \
      --template-body file://quick-deploy/aws-cloudformation.yaml
    ```

## Configuration

### Minimum Required Configuration

Edit your `.env` file with at least these values:

```bash
# LLM Provider (choose one or both)
ANTHROPIC_API_KEY=sk-ant-xxxxx     # Claude (recommended)
OPENAI_API_KEY=sk-xxxxx            # GPT-4 (alternative)

# Basic Settings
LLM_PROVIDER=anthropic             # or "openai"
DATABASE_URL=postgresql://localhost/ai_council
REDIS_URL=redis://localhost:6379
```

### Optional Configuration

For full features, add:

```bash
# Voice Synthesis
ELEVENLABS_API_KEY=xxxxx           # Premium voices

# Blockchain (for governance)
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
SOLANA_WALLET_PRIVATE_KEY=xxxxx

# Streaming
YOUTUBE_STREAM_KEY=xxxxx
TWITCH_STREAM_KEY=xxxxx
FACEBOOK_STREAM_KEY=xxxxx
```

## Your First Debate

### Using the CLI

The simplest way to run a debate:

```bash
# Basic debate
./ai-council debate start "Should we ban social media for children?"

# Customize agents and rounds
./ai-council debate start "Climate change solutions" \
  --agents 7 \
  --rounds 5 \
  --format structured

# Save output
./ai-council debate start "Universal Basic Income" \
  --agents 5 \
  --output debate_output.json
```

### Using Python

For more control:

```python
from core.debate_engine import DebateEngine
from core.agent_coordinator import AgentCoordinator
from core.config import Config

# Initialize
config = Config()
coordinator = AgentCoordinator(config)
engine = DebateEngine(coordinator, config)

# Run debate
debate = engine.create_debate(
    topic="Should AI be regulated?",
    agent_count=5,
    round_count=3
)

result = engine.run_debate(debate)
print(f"Consensus: {result.consensus_level:.2%}")
print(f"Summary: {result.summary}")
```

### Using the API

For integration with other systems:

```bash
# Create debate
curl -X POST http://localhost:8000/api/v1/debates \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Should AI be regulated?",
    "agent_count": 5,
    "round_count": 3
  }'

# Get debate status
curl http://localhost:8000/api/v1/debates/{debate_id}

# Get transcript
curl http://localhost:8000/api/v1/debates/{debate_id}/transcript
```

## Demo Modes

### Mock Mode (No API Costs)

Test the system without using API credits:

```bash
./ai-council demo --mock --duration 5
```

This runs a complete debate with simulated AI responses - perfect for testing!

### Budget Mode (Reduced Costs)

Use fewer agents and cheaper models:

```bash
export MAX_AGENTS=3
export LLM_PROVIDER=ollama  # Uses local models
./ai-council debate start "Test topic" --agents 3
```

### Production Mode

Full features with all agents:

```bash
./ai-council automation start --mode continuous
```

## Verify Installation

### Health Check

```bash
# CLI
./ai-council health

# API
curl http://localhost:8000/api/v1/health

# Expected response:
# {
#   "status": "healthy",
#   "checks": {
#     "database": "ok",
#     "redis": "ok",
#     "llm_provider": "ok"
#   }
# }
```

### Run Tests

```bash
# All tests
./scripts/test.sh all

# Specific suite
./scripts/test.sh unit
./scripts/test.sh integration
```

### View Logs

```bash
# Docker
docker-compose logs -f ai-council

# Python
tail -f logs/ai-council.log
```

## Common Issues

### "API Key Invalid"

**Problem**: LLM provider authentication failed

**Solution**:
```bash
# Verify keys are set
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY

# Test Anthropic key
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-haiku-20240307","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'
```

### "Database Connection Failed"

**Problem**: PostgreSQL not accessible

**Solution**:
```bash
# Start database
docker-compose up -d postgres

# Check connection
psql $DATABASE_URL -c "SELECT 1"
```

### "Out of Memory"

**Problem**: Insufficient RAM

**Solution**:
```bash
# Reduce agent count
export MAX_AGENTS=3

# Or increase Docker memory
docker update --memory 4g ai-council
```

### "Port Already in Use"

**Problem**: Port 8000 occupied

**Solution**:
```bash
# Use different port
export PORT=8080

# Or kill existing process
lsof -ti:8000 | xargs kill -9
```

## Next Steps

Now that you're up and running:

1. **[Create Your First Custom Debate](../user-guide/debates/creating.md)** - Learn advanced debate configuration
2. **[Set Up Automation](../user-guide/automation/overview.md)** - Enable 24/7 operation
3. **[Configure Streaming](../user-guide/streaming/setup.md)** - Stream to YouTube/Twitch
4. **[Explore the API](../api/overview.md)** - Integrate with your applications
5. **[Customize Personalities](../advanced/customization/personalities.md)** - Create unique AI agents

## Support

Need help?

- 📖 **Documentation**: [Full docs](../index.md)
- 💬 **Discord**: [Join community](https://discord.gg/aicouncil)
- 🐛 **Issues**: [Report bugs](https://github.com/your-org/ai-council-system/issues)
- 📧 **Email**: support@aicouncil.example.com

---

**Ready to dive deeper?** Check out the [User Guide](../user-guide/debates/creating.md) for advanced features!
