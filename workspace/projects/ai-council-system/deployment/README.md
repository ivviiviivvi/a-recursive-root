# AI Council System - Production Deployment Guide

Complete guide for deploying the AI Council System in production with 24/7 automated operation, multi-platform streaming, health monitoring, and analytics.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Deployment Methods](#deployment-methods)
- [Monitoring & Observability](#monitoring--observability)
- [Security](#security)
- [Backup & Recovery](#backup--recovery)
- [Troubleshooting](#troubleshooting)
- [Scaling](#scaling)

## Overview

The AI Council System production deployment provides:

- **24/7 Automated Operation**: Continuous debate scheduling and execution
- **Multi-Platform Streaming**: Simultaneous streaming to YouTube, Twitch, Facebook, and custom RTMP
- **Health Monitoring**: Real-time health checks with alerting
- **Analytics Dashboard**: Comprehensive metrics and performance insights
- **High Availability**: Redis caching, PostgreSQL persistence, automatic failover
- **Observability**: Prometheus metrics and Grafana dashboards
- **Security**: SSL/TLS, rate limiting, security headers, private metrics

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Internet                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Nginx Reverse Proxy (SSL/TLS, Rate Limiting)              │
│  - HTTP → HTTPS redirect                                    │
│  - API rate limiting (10 req/s)                            │
│  - WebSocket support                                        │
│  - Security headers                                         │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  AI Council Application (Python/FastAPI)                    │
│  - Debate scheduler & orchestrator                          │
│  - Multi-platform streamer                                  │
│  - Health monitoring                                        │
│  - Analytics engine                                         │
│  Ports: 8000 (API), 8080 (Metrics)                         │
└─────────────────────────────────────────────────────────────┘
           │                │                │
           ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│    Redis     │  │  PostgreSQL  │  │ Stream Outputs│
│   (Cache)    │  │ (Persistent) │  │ - YouTube    │
│              │  │              │  │ - Twitch     │
│  Port: 6379  │  │  Port: 5432  │  │ - Facebook   │
└──────────────┘  └──────────────┘  └──────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Observability Stack                                        │
│  ┌──────────────┐  ┌──────────────┐                       │
│  │  Prometheus  │─▶│   Grafana    │                       │
│  │  (Metrics)   │  │ (Dashboards) │                       │
│  │  Port: 9090  │  │  Port: 3000  │                       │
│  └──────────────┘  └──────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

### System Requirements

- **OS**: Linux (Ubuntu 20.04+ or similar)
- **CPU**: 4+ cores recommended (2 minimum)
- **RAM**: 8GB+ recommended (4GB minimum)
- **Disk**: 50GB+ available space
- **Network**: Stable internet connection with sufficient upload bandwidth for streaming

### Software Dependencies

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Git**: 2.x
- **systemd**: For service management (most Linux distributions)

### API Keys

- **Anthropic API Key**: For Claude AI personalities
- **OpenAI API Key**: For GPT-based personalities
- **ElevenLabs API Key**: For voice synthesis (optional)
- **YouTube Stream Key**: For YouTube streaming
- **Twitch Stream Key**: For Twitch streaming
- **Facebook Stream Key**: For Facebook streaming

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/your-org/ai-council-system.git
cd ai-council-system
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit with your API keys and configuration
nano .env
```

Required environment variables:

```bash
# AI API Keys
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
ELEVEN_API_KEY=your_elevenlabs_key  # Optional

# Streaming Keys
YOUTUBE_STREAM_KEY=your_youtube_key
TWITCH_STREAM_KEY=your_twitch_key
FACEBOOK_STREAM_KEY=your_facebook_key

# Database
POSTGRES_URL=postgresql://postgres:password@postgres:5432/ai_council
REDIS_URL=redis://redis:6379

# Automation
SCHEDULE_TYPE=adaptive  # adaptive, interval, cron, event_driven
MONITORING_INTERVAL=60  # seconds
LOG_LEVEL=info
```

### 3. SSL Certificates

For production HTTPS:

```bash
# Using Let's Encrypt (certbot)
sudo certbot certonly --standalone -d ai-council.example.com

# Copy certificates to deployment directory
sudo cp /etc/letsencrypt/live/ai-council.example.com/fullchain.pem deployment/ssl/
sudo cp /etc/letsencrypt/live/ai-council.example.com/privkey.pem deployment/ssl/
```

Or use self-signed certificates for testing:

```bash
mkdir -p deployment/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout deployment/ssl/privkey.pem \
  -out deployment/ssl/fullchain.pem
```

### 4. Deploy with Docker Compose

```bash
# Start all services
docker-compose -f deployment/docker-compose.production.yml up -d

# Check status
docker-compose -f deployment/docker-compose.production.yml ps

# View logs
docker-compose -f deployment/docker-compose.production.yml logs -f ai-council
```

### 5. Install Systemd Service (Optional)

For automatic startup on boot:

```bash
# Copy service file
sudo cp deployment/ai-council.service /etc/systemd/system/

# Create service user
sudo useradd -r -s /bin/false ai-council

# Set ownership
sudo chown -R ai-council:ai-council /opt/ai-council-system

# Enable and start service
sudo systemctl enable ai-council
sudo systemctl start ai-council

# Check status
sudo systemctl status ai-council
```

## Configuration

### Debate Scheduler

Edit scheduler configuration in `automation/scheduler.py` or via environment:

```python
config = ScheduleConfig(
    schedule_type=ScheduleType.ADAPTIVE,  # adaptive, interval, cron, event_driven
    interval_minutes=60,                  # For interval mode
    max_debates_per_day=24,
    quiet_hours_start=2,                  # 2 AM
    quiet_hours_end=6,                    # 6 AM
    adaptive_mode=True
)
```

### Streaming Configuration

Configure streaming platforms:

```python
# YouTube
youtube_config = StreamConfig(
    platform=StreamPlatform.YOUTUBE,
    stream_key=os.getenv("YOUTUBE_STREAM_KEY"),
    rtmp_url="rtmp://a.rtmp.youtube.com/live2",
    quality=StreamQuality.HIGH,  # 1080p
    enabled=True
)

# Twitch
twitch_config = StreamConfig(
    platform=StreamPlatform.TWITCH,
    stream_key=os.getenv("TWITCH_STREAM_KEY"),
    rtmp_url="rtmp://live.twitch.tv/app",
    quality=StreamQuality.HIGH,
    enabled=True
)
```

### Monitoring Configuration

Health check intervals and thresholds:

```python
monitor = HealthMonitor(
    check_interval_seconds=60,
    alert_threshold_consecutive_failures=3
)
```

## Deployment Methods

### Method 1: Docker Compose (Recommended)

Simple, self-contained deployment:

```bash
docker-compose -f deployment/docker-compose.production.yml up -d
```

**Pros**: Easy setup, isolated environment, portable
**Cons**: Single-server only

### Method 2: Systemd Service

System-level service with automatic restart:

```bash
sudo systemctl start ai-council
```

**Pros**: Automatic startup, system integration
**Cons**: Requires root access

### Method 3: Kubernetes (Advanced)

For multi-server deployments:

```bash
# Apply Kubernetes manifests (not included, requires adaptation)
kubectl apply -f k8s/
```

**Pros**: High availability, auto-scaling
**Cons**: Complex setup

## Monitoring & Observability

### Accessing Dashboards

- **Grafana**: `http://localhost:3000` (admin/admin)
- **Prometheus**: `http://localhost:9090`
- **Application API**: `https://your-domain.com/api`
- **Health Check**: `https://your-domain.com/health`

### Key Metrics

**Debate Metrics**:
- `debate_total`: Total debates executed
- `debate_active_count`: Currently active debates
- `debate_duration_seconds`: Debate duration histogram
- `debate_engagement_score`: Engagement score gauge

**Streaming Metrics**:
- `streaming_viewer_count`: Viewers per platform
- `streaming_bitrate_kbps`: Stream bitrate
- `streaming_frame_drop_rate`: Frame drop percentage
- `streaming_uptime_percent`: Stream uptime

**System Metrics**:
- `process_cpu_percent`: CPU usage
- `process_memory_bytes`: Memory usage
- `process_open_fds`: Open file descriptors
- `http_requests_total`: HTTP request count

### Alerts

Configure alerts in Prometheus or Grafana:

**Critical Alerts**:
- Stream failure on all platforms
- Database connection failure
- Memory usage > 95%
- Disk space < 5%

**Warning Alerts**:
- Stream failure on single platform
- Memory usage > 80%
- Disk space < 20%
- High frame drop rate (> 5%)

## Security

### Network Security

- **Firewall**: Only expose ports 80 (HTTP) and 443 (HTTPS)
- **Rate Limiting**: API limited to 10 req/s, general traffic to 100 req/s
- **DDoS Protection**: Use Cloudflare or similar for production

### SSL/TLS

- **Protocols**: TLSv1.2 and TLSv1.3 only
- **Ciphers**: HIGH:!aNULL:!MD5
- **HSTS**: Strict-Transport-Security header enabled

### Application Security

- **Secrets**: Never commit `.env` file
- **API Keys**: Rotate regularly
- **Database**: Use strong passwords, limit access
- **Metrics**: Metrics endpoint restricted to private networks only

### Security Headers

Applied automatically via nginx:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

## Backup & Recovery

### Database Backup

Automated PostgreSQL backups:

```bash
# Manual backup
docker exec ai-council-postgres pg_dump -U postgres ai_council > backup_$(date +%Y%m%d).sql

# Restore
docker exec -i ai-council-postgres psql -U postgres ai_council < backup_20250101.sql
```

### Automated Backup Script

```bash
#!/bin/bash
# /opt/ai-council-system/scripts/backup.sh

BACKUP_DIR="/opt/ai-council-system/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Database backup
docker exec ai-council-postgres pg_dump -U postgres ai_council | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# Data directory backup
tar -czf "$BACKUP_DIR/data_$DATE.tar.gz" /opt/ai-council-system/data

# Cleanup old backups (keep 30 days)
find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete
```

Add to crontab:

```bash
0 2 * * * /opt/ai-council-system/scripts/backup.sh
```

## Troubleshooting

### Common Issues

#### Debate Not Starting

```bash
# Check scheduler logs
docker-compose logs ai-council | grep scheduler

# Check system health
curl http://localhost:8000/health

# Verify schedule
docker exec ai-council-main python -c "from automation import DebateScheduler; s = DebateScheduler(); print(s.get_statistics())"
```

#### Stream Not Working

```bash
# Check streaming logs
docker-compose logs ai-council | grep streaming

# Verify stream keys
docker exec ai-council-main env | grep STREAM_KEY

# Test RTMP connectivity
ffmpeg -f lavfi -i testsrc -t 10 -f flv "rtmp://a.rtmp.youtube.com/live2/YOUR_KEY"
```

#### High Memory Usage

```bash
# Check container memory
docker stats

# Restart service
docker-compose restart ai-council

# Clear voice cache
docker exec ai-council-main rm -rf /app/voice_cache/*
```

#### Database Connection Issues

```bash
# Check PostgreSQL status
docker-compose logs postgres

# Verify connection
docker exec ai-council-postgres pg_isready -U postgres

# Reset database
docker-compose down
docker volume rm ai-council-system_postgres-data
docker-compose up -d
```

### Log Locations

- **Application**: `/opt/ai-council-system/logs/`
- **Nginx**: `/var/log/nginx/`
- **Docker**: `docker-compose logs -f SERVICE_NAME`

## Scaling

### Vertical Scaling

Increase resources for single server:

```yaml
# docker-compose.production.yml
services:
  ai-council:
    deploy:
      resources:
        limits:
          cpus: '8'
          memory: 16G
        reservations:
          cpus: '4'
          memory: 8G
```

### Horizontal Scaling

For multi-server deployments:

1. **Separate streaming servers**: Dedicate servers per platform
2. **Load balancer**: Add nginx upstream servers
3. **Shared storage**: Use NFS or S3 for recordings
4. **Database replication**: PostgreSQL master-replica setup
5. **Redis cluster**: Redis Sentinel or Cluster mode

### Performance Optimization

- **Enable voice caching**: Reduces TTS API calls
- **Use CDN**: CloudFare or similar for static content
- **Database indexes**: Already optimized in init.sql
- **Connection pooling**: PostgreSQL connection pool size
- **Redis persistence**: Adjust RDB/AOF settings

## Maintenance

### Regular Tasks

**Daily**:
- Check system health dashboard
- Review error logs
- Verify streaming status

**Weekly**:
- Review analytics insights
- Check disk space
- Update stream keys if needed

**Monthly**:
- Update dependencies
- Rotate API keys
- Review and archive old debates
- Database vacuum/optimization

### Updates

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose -f deployment/docker-compose.production.yml build

# Restart services
docker-compose -f deployment/docker-compose.production.yml up -d
```

## Support

For issues and questions:

- **Documentation**: `/docs` directory
- **Examples**: `/examples` directory
- **Issues**: GitHub Issues
- **Logs**: Check application and container logs first

## License

[Your License Here]

---

**AI Council System** - Automated Debate Platform
Phase 5: Automation & Scale - Production Ready ✅
