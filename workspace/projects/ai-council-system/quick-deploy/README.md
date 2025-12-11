# Live Demo Quick Deploy

One-click deployment configurations for running a live AI Council System demo.

## Deployment Options

### 1. DigitalOcean (Recommended for Quick Start)

**Cost**: ~$24/month
**Setup Time**: 5 minutes
**Best For**: Testing, small demos, development

[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/your-org/ai-council-system/tree/main)

**Manual Setup**:
```bash
# 1. Create Droplet (4GB RAM, 2 vCPUs)
doctl compute droplet create ai-council-demo \
  --region nyc3 \
  --size s-2vcpu-4gb \
  --image docker-20-04 \
  --ssh-keys YOUR_SSH_KEY_ID

# 2. SSH into droplet
doctl compute ssh ai-council-demo

# 3. Deploy with script
curl -fsSL https://raw.githubusercontent.com/your-org/ai-council-system/main/quick-deploy/digitalocean-setup.sh | bash
```

### 2. AWS EC2 + CloudFormation

**Cost**: ~$30-40/month
**Setup Time**: 10 minutes
**Best For**: Production demos, scalability testing

```bash
# Deploy using CloudFormation
aws cloudformation create-stack \
  --stack-name ai-council-demo \
  --template-body file://quick-deploy/aws-cloudformation.yaml \
  --parameters file://quick-deploy/aws-params.json \
  --capabilities CAPABILITY_IAM

# Get public IP
aws cloudformation describe-stacks \
  --stack-name ai-council-demo \
  --query 'Stacks[0].Outputs[?OutputKey==`PublicIP`].OutputValue' \
  --output text
```

### 3. Google Cloud Platform (Cloud Run)

**Cost**: Pay-as-you-go (~$10-50/month)
**Setup Time**: 8 minutes
**Best For**: Auto-scaling, serverless deployment

```bash
# Deploy to Cloud Run
gcloud run deploy ai-council-demo \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2 \
  --min-instances 0 \
  --max-instances 3

# Get URL
gcloud run services describe ai-council-demo \
  --region us-central1 \
  --format 'value(status.url)'
```

### 4. Heroku (Simplest, No DevOps)

**Cost**: ~$25-50/month
**Setup Time**: 3 minutes
**Best For**: Non-technical users, rapid prototyping

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/your-org/ai-council-system)

**Manual**:
```bash
# 1. Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# 2. Login and create app
heroku login
heroku create ai-council-demo

# 3. Deploy
git push heroku main

# 4. Scale up
heroku ps:scale web=1:standard-2x
```

### 5. Docker Compose (Local/Self-Hosted)

**Cost**: Free (own hardware) or VPS cost
**Setup Time**: 5 minutes
**Best For**: Self-hosting, testing, development

```bash
# 1. Clone repository
git clone https://github.com/your-org/ai-council-system.git
cd ai-council-system

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Deploy with quick-deploy script
./quick-deploy/local-docker.sh

# Or manually:
docker-compose -f docker/docker-compose.yml up -d
```

### 6. Kubernetes (Production-Ready)

**Cost**: ~$100-300/month
**Setup Time**: 20 minutes
**Best For**: Production, high availability, scale

```bash
# Deploy to existing K8s cluster
kubectl apply -f quick-deploy/k8s/

# Or use Helm chart
helm install ai-council ./quick-deploy/helm/ \
  --namespace ai-council \
  --create-namespace \
  --set apiKeys.anthropic=YOUR_KEY \
  --set apiKeys.openai=YOUR_KEY
```

---

## Configuration

All deployments require these API keys as environment variables:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx

# Optional (for full features)
ELEVENLABS_API_KEY=xxxxx
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
YOUTUBE_STREAM_KEY=xxxxx
TWITCH_STREAM_KEY=xxxxx
```

## Demo Modes

### Quick Demo (Mock Mode)
```bash
# No API costs - uses mock responses
export DEMO_MODE=mock
./ai-council demo --mock --duration 5
```

### Limited Demo (Budget Mode)
```bash
# Uses cheaper models and fewer agents
export DEMO_MODE=budget
export MAX_AGENTS=5
export LLM_PROVIDER=ollama
./ai-council demo --agents 5 --rounds 2
```

### Full Demo (Production Mode)
```bash
# Full features with all agents
export DEMO_MODE=production
./ai-council automation start --mode test --duration 30m
```

---

## Post-Deployment

### 1. Verify Installation
```bash
# Check health
curl http://YOUR_IP:8000/api/v1/health

# Run test debate
curl -X POST http://YOUR_IP:8000/api/v1/debates \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test Debate", "agent_count": 3, "round_count": 1}'
```

### 2. Access UI
- Dashboard: `http://YOUR_IP:8000/dashboard`
- API Docs: `http://YOUR_IP:8000/docs`
- Streaming: `http://YOUR_IP:8000/stream`

### 3. Monitor Logs
```bash
# Docker Compose
docker-compose logs -f ai-council

# Kubernetes
kubectl logs -f -l app=ai-council -n ai-council

# Heroku
heroku logs --tail --app ai-council-demo
```

### 4. First Debate
```bash
# Using CLI
./ai-council debate start "Should AI be regulated?" --agents 5 --rounds 3

# Using API
curl -X POST http://YOUR_IP:8000/api/v1/debates \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Should AI be regulated?",
    "agent_count": 5,
    "round_count": 3
  }'
```

---

## Troubleshooting

### Common Issues

**1. "API Key Invalid"**
```bash
# Verify keys are set
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY

# Test key validity
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-haiku-20240307","max_tokens":10,"messages":[{"role":"user","content":"test"}]}'
```

**2. "Out of Memory"**
```bash
# Increase memory allocation
docker update --memory 4g ai-council
# Or scale up your instance size
```

**3. "Port Already in Use"**
```bash
# Change port
export PORT=8080
# Or kill existing process
lsof -ti:8000 | xargs kill -9
```

**4. "Database Connection Failed"**
```bash
# Check PostgreSQL is running
docker ps | grep postgres
# Restart database
docker-compose restart postgres
```

---

## Cost Optimization

### Minimize API Costs
```bash
# Use local models (Ollama)
export LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434

# Reduce agent count
export MAX_AGENTS=5

# Limit debate frequency
export MIN_DEBATE_INTERVAL=3600  # 1 hour
```

### Use Free Tiers
- **Anthropic**: $5 free credit (new accounts)
- **OpenAI**: $5 free credit (new accounts)
- **ElevenLabs**: 10,000 characters/month free
- **Heroku**: Free tier available (limited hours)
- **DigitalOcean**: $200 credit (new accounts, 60 days)

### Scheduled Shutdown
```bash
# Auto-shutdown during off-hours
crontab -e
# Add: 0 22 * * * docker-compose down  # Shutdown at 10 PM
# Add: 0 8 * * * docker-compose up -d  # Start at 8 AM
```

---

## Support

- **Documentation**: https://docs.aicouncil.example.com
- **Issues**: https://github.com/your-org/ai-council-system/issues
- **Discord**: [Join our community](DISCORD_LINK)
- **Email**: support@aicouncil.example.com

---

## Security Notes

⚠️ **For Demo/Testing Only** - Additional security hardening required for production:

1. Enable authentication on API endpoints
2. Configure SSL/TLS certificates
3. Set up firewall rules
4. Enable rate limiting
5. Configure CORS properly
6. Use secrets management (Vault, AWS Secrets Manager)
7. Enable audit logging
8. Set up automated backups

See `docs/SECURITY.md` for production security checklist.

---

**Quick Links**:
- [Full Documentation](../docs/)
- [Developer Guide](../DEVELOPER_GUIDE.md)
- [Cost Analysis](../COST_ANALYSIS.md)
- [Production Deployment](../deployment/)
