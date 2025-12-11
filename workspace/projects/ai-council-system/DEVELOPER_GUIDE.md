# AI Council System - Developer Guide

**Version**: 2.0.0
**Last Updated**: 2025-10-26

Complete developer guide for working with the AI Council System.

---

## Table of Contents

- [Quick Start for Developers](#quick-start-for-developers)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [CLI Reference](#cli-reference)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Performance](#performance)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## Quick Start for Developers

### Option 1: GitHub Codespaces (Fastest)

```bash
# Click "Open in GitHub Codespaces" button in README
# Wait for automatic setup (2-3 minutes)
# Add API keys to .env
# Start developing!
```

### Option 2: Local Setup

```bash
# Clone repository
git clone https://github.com/your-org/ai-council-system.git
cd ai-council-system

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run tests to verify setup
./scripts/test.sh unit

# Try a demo
./quick-start.sh
```

---

## Project Structure

```
ai-council-system/
├── 📁 core/                    # Core debate engine
│   ├── agents/                 # AI agents & LLM providers
│   ├── council/                # Debate orchestration
│   └── events/                 # Event ingestion
│
├── 📁 blockchain/              # Blockchain integration
│   ├── token/                  # Tokenomics & governance
│   ├── rng/                    # Decentralized RNG
│   └── integrations/           # Blockchain clients
│
├── 📁 streaming/               # Media production
│   ├── avatars/                # Visual personalities
│   ├── voices/                 # Voice synthesis
│   ├── backgrounds/            # Dynamic backgrounds
│   └── effects/                # Video effects
│
├── 📁 automation/              # Automation & scale
│   ├── scheduler.py            # Debate scheduling
│   ├── streaming.py            # Multi-platform streaming
│   ├── monitoring.py           # Health monitoring
│   ├── analytics.py            # Performance analytics
│   └── orchestrator.py         # Master orchestrator
│
├── 📁 deployment/              # Production infrastructure
│   ├── docker-compose.production.yml
│   ├── nginx.conf
│   ├── init.sql
│   └── grafana-dashboards/
│
├── 📁 api/                     # API definitions
│   └── openapi.yaml            # OpenAPI/Swagger spec
│
├── 📁 examples/                # Example code
│   ├── demo_debate.py
│   ├── end_to_end_integration.py
│   └── phase5_complete_demo.py
│
├── 📁 tests/                   # Test suite
│   ├── unit/
│   ├── integration/
│   └── performance/
│
├── 📁 scripts/                 # Automation scripts
│   ├── deploy.sh
│   └── test.sh
│
├── 📁 web/                     # Web interface
│   └── backend/
│
├── 📄 ai-council               # Main CLI tool
├── 📄 quick-start.sh           # Interactive launcher
├── 📄 .devcontainer/           # Codespaces config
└── 📄 docs/                    # Documentation
```

---

## Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/my-new-feature

# Make changes
# ...

# Run tests
./scripts/test.sh all

# Commit
git add .
git commit -m "Add my new feature"

# Push
git push origin feature/my-new-feature
```

### 2. Adding a New AI Personality

```python
# In core/agents/personalities.py

from core.agents import Personality

new_personality = Personality(
    name="The New Personality",
    description="Description of personality",
    debate_style="Communication style",
    core_values=["value1", "value2"],
    expertise_areas=["area1", "area2"],
    communication_style="Style description",
    bias_tendencies=["tendency1"],
    typical_arguments=["argument style"],
    interaction_patterns={
        "formal": 0.7,
        "collaborative": 0.8
    }
)

# Add to DEFAULT_PERSONALITIES dict
DEFAULT_PERSONALITIES["The New Personality"] = new_personality
```

### 3. Adding a New Health Check

```python
# In automation/monitoring.py

async def check_my_component():
    """Check health of my component"""
    try:
        # Perform check
        status = HealthStatus.HEALTHY
        message = "Component is healthy"
    except Exception as e:
        status = HealthStatus.UNHEALTHY
        message = str(e)

    return HealthCheck(
        name="my_component",
        status=status,
        message=message,
        timestamp=datetime.now()
    )

# Register check
monitor.register_check("my_component", check_my_component)
```

### 4. Adding a New Streaming Platform

```python
# In automation/streaming.py

class NewPlatformDestination(StreamDestination):
    """Streaming destination for New Platform"""

    def __init__(self, config: StreamConfig):
        super().__init__(config)
        # Platform-specific setup

    async def start_stream(self):
        # Implement streaming logic
        pass

    async def stop_stream(self):
        # Implement stop logic
        pass

# Add to MultiPlatformStreamer
```

---

## CLI Reference

### Main Commands

```bash
# Debate Management
./ai-council debate "Topic" --agents 5 --rounds 3
./ai-council list-personalities
./ai-council interactive

# Automation
./ai-council automate --mode continuous
./ai-council schedule list
./ai-council schedule add --topic "Topic" --time "2025-10-26T14:00:00"

# Streaming
./ai-council stream --platforms youtube twitch
./ai-council stream-status
./ai-council test-stream

# Health & Monitoring
./ai-council health --all
./ai-council status
./ai-council monitor --interval 60

# Analytics
./ai-council analytics --period day
./ai-council export results.json --format json
./ai-council report

# System Administration
./ai-council init
./ai-council config --show
./ai-council deploy --mode docker
./ai-council backup backup.tar.gz
./ai-council clean --cache
```

### Interactive Quick Start

```bash
./quick-start.sh

# Choose from:
# 1. Quick Debate Demo
# 2. Avatar System Demo
# 3. Video Effects Demo
# 4. Voice Cloning Demo
# 5. Dynamic Backgrounds Demo
# 6. Full Automation Demo
# 7. Comprehensive Integration
# 8. Start Production Services
# 9. View System Status
```

---

## API Reference

Full OpenAPI/Swagger specification: `api/openapi.yaml`

### Key Endpoints

**Debates**
- `GET /api/v1/debates` - List debates
- `POST /api/v1/debates` - Create debate
- `GET /api/v1/debates/{id}` - Get debate details
- `GET /api/v1/debates/{id}/transcript` - Get transcript

**Automation**
- `POST /api/v1/automation/start` - Start automation
- `POST /api/v1/automation/stop` - Stop automation
- `GET /api/v1/automation/status` - Get status

**Streaming**
- `POST /api/v1/streaming/start` - Start streaming
- `POST /api/v1/streaming/stop` - Stop streaming
- `GET /api/v1/streaming/status` - Get streaming status

**Health & Analytics**
- `GET /api/v1/health` - System health
- `GET /api/v1/analytics/dashboard` - Dashboard data
- `GET /api/v1/analytics/debates` - Debate analytics

### Example API Usage

```python
import requests

# Start a debate
response = requests.post(
    "http://localhost:8000/api/v1/debates",
    json={
        "topic": "The Future of AI",
        "agent_count": 5,
        "round_count": 3
    },
    headers={"X-API-Key": "your_api_key"}
)

debate_id = response.json()["debate_id"]

# Check debate status
status = requests.get(
    f"http://localhost:8000/api/v1/debates/{debate_id}"
)

print(status.json())
```

---

## Testing

### Running Tests

```bash
# All tests
./scripts/test.sh all

# Specific suite
./scripts/test.sh unit
./scripts/test.sh integration
./scripts/test.sh performance

# With coverage
./scripts/test.sh coverage

# Code quality
./scripts/test.sh quality
```

### Writing Tests

**Unit Test Example:**

```python
# tests/unit/test_my_feature.py

import pytest
from my_module import my_function

class TestMyFeature:
    def test_basic_functionality(self):
        result = my_function("input")
        assert result == "expected"

    @pytest.mark.asyncio
    async def test_async_function(self):
        result = await async_function()
        assert result is not None
```

**Integration Test Example:**

```python
# tests/integration/test_workflow.py

import pytest

class TestWorkflow:
    @pytest.mark.asyncio
    async def test_complete_workflow(
        self,
        sample_council,
        mock_debate_data
    ):
        result = await sample_council.run_debate(
            topic=mock_debate_data["topic"],
            rounds=3
        )

        assert result is not None
        assert len(result["rounds"]) == 3
```

---

## Performance

### Running Benchmarks

```bash
# Full benchmark suite
python tests/performance/benchmark.py

# Via test script
./scripts/test.sh performance
```

### Performance Targets

- **Debate Generation**: < 30s per round (15 agents)
- **Avatar Rendering**: < 100ms per frame
- **Voice Synthesis**: < 2s per response (< 50ms cached)
- **Stream Latency**: 2-5s end-to-end
- **API Response Time**: < 100ms (p95)
- **System Uptime**: > 99.9%

### Optimization Tips

1. **Enable Caching**: Voice, avatar, and background caching
2. **Use Async**: All I/O operations should be async
3. **Connection Pooling**: Database and API connections
4. **CDN**: For static assets in production
5. **Load Balancing**: Multiple worker instances

---

## Deployment

### Development

```bash
./scripts/deploy.sh development
```

### Docker

```bash
./scripts/deploy.sh docker
```

### Production

```bash
# Docker Compose only
./scripts/deploy.sh production

# With systemd service
sudo ./scripts/deploy.sh production --systemd
```

### Environment Variables

Required:
```bash
ANTHROPIC_API_KEY=sk-ant-...  # OR
OPENAI_API_KEY=sk-...
```

Optional:
```bash
ELEVEN_API_KEY=...
YOUTUBE_STREAM_KEY=...
TWITCH_STREAM_KEY=...
FACEBOOK_STREAM_KEY=...

POSTGRES_URL=postgresql://...
REDIS_URL=redis://...

SCHEDULE_TYPE=adaptive
MONITORING_INTERVAL=60
LOG_LEVEL=info
```

---

## Contributing

### Code Style

- **Python**: PEP 8, use Black formatter
- **Docstrings**: Google style
- **Type Hints**: Use for all function signatures
- **Async**: Prefer async/await for I/O

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Make changes
4. Run tests (`./scripts/test.sh all`)
5. Update documentation
6. Submit PR with clear description

### Areas for Contribution

- Additional AI personalities
- New streaming platforms
- Enhanced visual effects
- Multi-language support
- Performance optimizations
- Documentation improvements
- Bug fixes

---

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure project root in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**API Key Issues**
```bash
# Verify .env file
cat .env | grep API_KEY

# Test API key
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY'))"
```

**Docker Issues**
```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Port Conflicts**
```bash
# Check port usage
netstat -tlnp | grep :8000

# Change port in docker-compose.yml
```

---

## Additional Resources

- **README.md**: Project overview
- **COMPILATION.md**: Complete project breakdown
- **deployment/README.md**: Production deployment guide
- **api/openapi.yaml**: API specification
- **examples/**: Code examples

---

## Support

- **Documentation**: This guide + linked docs
- **Examples**: `examples/` directory
- **Tests**: `tests/` directory for patterns
- **Issues**: GitHub Issues
- **API Docs**: `api/openapi.yaml`

---

**Happy Developing! 🚀**

AI Council System v2.0.0 - Where AI Agents Debate, Humanity Decides
