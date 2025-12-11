# Automation & Scale System

**Phase 5.1** - 24/7 automated operation for AI Council debates

Provides complete automation infrastructure for continuous debate operation with multi-platform streaming, intelligent scheduling, health monitoring, and comprehensive analytics.

---

## 🎯 Overview

The Automation & Scale system enables fully automated 24/7 debate operation with:

1. **Automated Scheduler** - Intelligent debate scheduling with multiple strategies
2. **Multi-Platform Streaming** - Simultaneous streaming to YouTube, Twitch, Facebook
3. **Health Monitoring** - Continuous health checks with automatic alerting
4. **Analytics Dashboard** - Real-time and historical performance metrics

Together, these provide enterprise-grade automation for production deployment.

---

## 📊 Features

### Automated Scheduling
- ✅ Multiple scheduling strategies (interval, cron, adaptive, event-driven)
- ✅ Quiet hours configuration
- ✅ Maximum debates per day limits
- ✅ Automatic retry on failure
- ✅ Event-triggered scheduling
- ✅ Schedule persistence

### Multi-Platform Streaming
- ✅ Simultaneous streaming to 5+ platforms
- ✅ Automatic failover and retry
- ✅ Adaptive bitrate management
- ✅ Stream health monitoring
- ✅ Recording to local files
- ✅ Viewer statistics tracking

### Health Monitoring
- ✅ Periodic health checks
- ✅ Component-level monitoring
- ✅ Automatic alert generation
- ✅ Alert severity levels (info, warning, error, critical)
- ✅ Health history tracking
- ✅ Uptime monitoring

### Analytics & Metrics
- ✅ Debate performance tracking
- ✅ Streaming metrics (viewers, bitrate, uptime)
- ✅ System resource monitoring
- ✅ Trend analysis
- ✅ Performance insights
- ✅ Exportable reports

---

## 🚀 Quick Start

### Basic Automation Setup

```python
from automation import (
    DebateScheduler,
    ScheduleConfig,
    ScheduleType,
    MultiPlatformStreamer,
    HealthMonitor,
    AnalyticsDashboard
)
from datetime import datetime

# 1. Setup Scheduler
config = ScheduleConfig(
    schedule_type=ScheduleType.ADAPTIVE,
    interval_minutes=60,
    max_debates_per_day=24
)
scheduler = DebateScheduler(config)

# Generate schedule
scheduler.generate_schedule(datetime.now(), duration_hours=24)

# 2. Setup Streaming
streamer = MultiPlatformStreamer()
streamer.add_destination(StreamConfig(
    platform=StreamPlatform.YOUTUBE,
    stream_key="your-stream-key",
    rtmp_url="rtmp://a.rtmp.youtube.com/live2"
))

# 3. Setup Monitoring
monitor = HealthMonitor(check_interval_seconds=60)
monitor.register_check("scheduler", check_scheduler_health)

# 4. Setup Analytics
dashboard = AnalyticsDashboard(data_dir=Path("analytics_data"))

# 5. Start Automation
await scheduler.start()
await monitor.start_monitoring()
```

### Running the Demo

```bash
cd workspace/projects/ai-council-system
python examples/automation_demo.py
```

Demonstrates:
- Automated debate scheduling
- Multi-platform streaming setup
- Health monitoring with alerts
- Analytics dashboard
- Complete integrated automation

---

## 📖 API Reference

### DebateScheduler

Automated debate scheduling with multiple strategies.

```python
scheduler = DebateScheduler(config=ScheduleConfig(
    schedule_type=ScheduleType.ADAPTIVE,
    interval_minutes=60,
    max_debates_per_day=24,
    quiet_hours_start=2,
    quiet_hours_end=6
))
```

#### Methods

**generate_schedule(start_time, duration_hours) → List[ScheduledDebate]**

Generate debate schedule for a time period.

```python
debates = scheduler.generate_schedule(
    start_time=datetime.now(),
    duration_hours=24
)
```

**schedule_debate(scheduled_time, topic=None) → ScheduledDebate**

Manually schedule a debate.

```python
debate = scheduler.schedule_debate(
    scheduled_time=datetime.now() + timedelta(hours=1),
    topic="AI Regulation"
)
```

**start() → async**

Start the automated scheduler (runs continuously).

```python
await scheduler.start()  # Runs until stopped
```

**get_statistics() → Dict**

Get scheduler statistics.

```python
stats = scheduler.get_statistics()
# {
#     'total_scheduled': 48,
#     'pending': 23,
#     'completed': 20,
#     'failed': 2,
#     'success_rate': 90.9
# }
```

### MultiPlatformStreamer

Simultaneous streaming to multiple platforms.

```python
streamer = MultiPlatformStreamer()
```

#### Methods

**add_destination(config) → StreamDestination**

Add a streaming destination.

```python
youtube = streamer.add_destination(StreamConfig(
    platform=StreamPlatform.YOUTUBE,
    stream_key="ytlive-xxxx-xxxx",
    rtmp_url="rtmp://a.rtmp.youtube.com/live2",
    quality=StreamQuality.HIGH
))
```

**start_streaming(recording_path=None) → async**

Start streaming to all destinations.

```python
await streamer.start_streaming(
    recording_path=Path("recordings/debate.mp4")
)
```

**stop_streaming() → async**

Stop all streams.

```python
await streamer.stop_streaming()
```

**get_statistics() → Dict**

Get streaming statistics.

```python
stats = streamer.get_statistics()
# {
#     'live_destinations': 3,
#     'total_viewers': 1250,
#     'average_bitrate_kbps': 6000
# }
```

### HealthMonitor

Continuous health monitoring with alerts.

```python
monitor = HealthMonitor(check_interval_seconds=60)
```

#### Methods

**register_check(name, check_fn)**

Register a health check function.

```python
async def check_api():
    # Return (is_healthy, message)
    return True, "API responding"

monitor.register_check("api", check_api)
```

**run_check(name) → HealthCheck**

Run a specific check.

```python
result = await monitor.run_check("api")
print(f"Status: {result.status.value}")
```

**start_monitoring() → async**

Start continuous monitoring.

```python
await monitor.start_monitoring()  # Runs continuously
```

**get_statistics() → Dict**

Get monitoring statistics.

```python
stats = monitor.get_statistics()
# {
#     'overall_status': 'healthy',
#     'total_checks': 1240,
#     'active_alerts': 0
# }
```

### AnalyticsDashboard

Comprehensive analytics and metrics.

```python
dashboard = AnalyticsDashboard(data_dir=Path("analytics"))
```

#### Methods

**record_debate(metrics)**

Record debate metrics.

```python
from automation import DebateMetrics

metrics = DebateMetrics(
    debate_id="debate_123",
    start_time=datetime.now(),
    duration_seconds=1800,
    engagement_score=0.85,
    viewer_count_peak=500
)
dashboard.record_debate(metrics)
```

**get_debate_statistics(days=7) → Dict**

Get debate statistics.

```python
stats = dashboard.get_debate_statistics(days=7)
# {
#     'total_debates': 42,
#     'avg_engagement': 0.78,
#     'peak_viewers': 1250
# }
```

**get_dashboard_data() → Dict**

Get complete dashboard data.

```python
data = dashboard.get_dashboard_data()
# Includes debates, streaming, system, trends, insights
```

**export_report(output_path, days=30)**

Export analytics report.

```python
dashboard.export_report(
    output_path=Path("reports/monthly.json"),
    days=30
)
```

---

## 🗓️ Scheduling Strategies

### Interval Scheduling

Fixed time intervals between debates.

```python
config = ScheduleConfig(
    schedule_type=ScheduleType.INTERVAL,
    interval_minutes=60  # Debate every hour
)
```

### Adaptive Scheduling

AI-optimized scheduling based on peak engagement times.

```python
config = ScheduleConfig(
    schedule_type=ScheduleType.ADAPTIVE,
    # Automatically schedules at: 9AM, 12PM, 3PM, 6PM, 9PM
)
```

### Event-Driven Scheduling

Triggered by trending topics or events.

```python
scheduler = EventTriggeredScheduler(config)
scheduler.trigger_debate_from_event({
    "topic": "Breaking News Event",
    "urgency": "high"
})
```

### Quiet Hours

Avoid scheduling during specified hours.

```python
config = ScheduleConfig(
    quiet_hours_start=2,  # 2 AM
    quiet_hours_end=6     # 6 AM
)
```

---

## 📡 Streaming Platforms

### YouTube Live

```python
youtube = StreamConfig(
    platform=StreamPlatform.YOUTUBE,
    stream_key="ytlive-xxxx-xxxx-xxxx-xxxx",
    rtmp_url="rtmp://a.rtmp.youtube.com/live2",
    quality=StreamQuality.HIGH  # 1080p, 6000 kbps
)
```

### Twitch

```python
twitch = StreamConfig(
    platform=StreamPlatform.TWITCH,
    stream_key="live_xxxxxxxxxxxx",
    rtmp_url="rtmp://live.twitch.tv/app",
    quality=StreamQuality.HIGH
)
```

### Facebook Live

```python
facebook = StreamConfig(
    platform=StreamPlatform.FACEBOOK,
    stream_key="FB-xxxxxxxxxxxx",
    rtmp_url="rtmps://live-api-s.facebook.com:443/rtmp",
    quality=StreamQuality.MEDIUM  # 720p, 3000 kbps
)
```

### Custom RTMP

```python
custom = StreamConfig(
    platform=StreamPlatform.CUSTOM_RTMP,
    stream_key="custom-key",
    rtmp_url="rtmp://your-server.com/live",
    quality=StreamQuality.HIGH
)
```

### Stream Quality Presets

| Quality | Resolution | Bitrate | FPS |
|---------|-----------|---------|-----|
| LOW | 480p | 1500 kbps | 30 |
| MEDIUM | 720p | 3000 kbps | 30 |
| HIGH | 1080p | 6000 kbps | 30 |
| ULTRA | 4K | 15000 kbps | 60 |

---

## 💚 Health Checks

### Predefined Checks

```python
from automation import (
    check_scheduler_health,
    check_streaming_health,
    check_database_health,
    check_disk_space,
    check_memory_usage,
    check_api_endpoints,
    check_event_ingestion,
    check_tts_availability
)

monitor.register_check("scheduler", check_scheduler_health)
monitor.register_check("disk", check_disk_space)
```

### Custom Health Checks

```python
async def check_custom_service() -> tuple[bool, str]:
    """Custom health check"""
    try:
        # Check your service
        response = await ping_service()
        return True, "Service healthy"
    except Exception as e:
        return False, f"Service error: {e}"

monitor.register_check("custom", check_custom_service)
```

### Alert Callbacks

```python
async def on_alert(alert):
    """Handle alerts"""
    if alert.severity == AlertSeverity.CRITICAL:
        # Send notification
        send_pager_alert(alert.message)
    elif alert.severity == AlertSeverity.WARNING:
        # Log warning
        logger.warn(alert.message)

monitor.on_alert = on_alert
```

---

## 📊 Analytics & Insights

### Debate Metrics Tracked

- Duration and completion rate
- Participant count and diversity
- Response quality (length, confidence)
- Viewer engagement
- Consensus and controversy levels
- Topic trends

### Streaming Metrics Tracked

- Viewer counts (peak and average)
- Bitrate and quality metrics
- Uptime percentage
- Frame drop rates
- Platform-specific performance
- Total bytes sent

### System Metrics Tracked

- CPU, memory, disk usage
- Network throughput
- Active debates and streams
- Resource utilization trends

### Performance Insights

```python
insights = dashboard.get_performance_insights()

# {
#     'health': 'good',
#     'highlights': [
#         'High engagement levels maintained',
#         'Peak viewership: 1250 viewers'
#     ],
#     'recommendations': [
#         'Consider scaling for peak hours'
#     ]
# }
```

---

## 🔧 Production Deployment

### Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export YOUTUBE_STREAM_KEY="ytlive-xxxx"
export TWITCH_STREAM_KEY="live_xxxx"
export MONITORING_INTERVAL=60
export ANALYTICS_DIR="/var/lib/ai-council/analytics"
```

### Systemd Service

```ini
[Unit]
Description=AI Council Automation
After=network.target

[Service]
Type=simple
User=ai-council
WorkingDirectory=/opt/ai-council
ExecStart=/opt/ai-council/venv/bin/python -m automation.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "automation.main"]
```

### Monitoring Integration

```python
# Integrate with Prometheus
from prometheus_client import Counter, Histogram, Gauge

debates_total = Counter('debates_total', 'Total debates run')
debate_duration = Histogram('debate_duration_seconds', 'Debate duration')
active_streams = Gauge('active_streams', 'Currently active streams')
```

---

## 🎬 Integration Example

### Complete Automation Loop

```python
import asyncio
from automation import *

async def run_automated_system():
    """Run complete automated system"""

    # Initialize components
    scheduler = DebateScheduler(ScheduleConfig(
        schedule_type=ScheduleType.ADAPTIVE,
        interval_minutes=60
    ))

    streamer = MultiPlatformStreamer()
    streamer.add_destination(youtube_config)
    streamer.add_destination(twitch_config)

    monitor = HealthMonitor()
    monitor.register_check("scheduler", check_scheduler_health)
    monitor.register_check("streaming", check_streaming_health)

    dashboard = AnalyticsDashboard(Path("analytics"))

    # Setup callbacks
    async def on_debate_start(debate):
        # Start streaming
        await streamer.start_streaming()

    async def on_debate_complete(debate):
        # Record metrics
        metrics = DebateMetrics(
            debate_id=debate.debate_id,
            start_time=debate.actual_start_time,
            end_time=debate.actual_end_time,
            # ... more metrics
        )
        dashboard.record_debate(metrics)

        # Stop streaming
        await streamer.stop_streaming()

    scheduler.set_callbacks(
        on_start=on_debate_start,
        on_complete=on_debate_complete
    )

    # Start all systems
    await asyncio.gather(
        scheduler.start(),
        monitor.start_monitoring()
    )

# Run
asyncio.run(run_automated_system())
```

---

## 📈 Performance Optimization

### Scheduler Optimization

```python
# Use adaptive scheduling for peak times
config = ScheduleConfig(
    schedule_type=ScheduleType.ADAPTIVE,
    min_interval_minutes=30  # Minimum gap between debates
)

# Clear completed debates
scheduler.clear_completed()
```

### Streaming Optimization

```python
# Enable adaptive bitrate
bitrate_manager = AdaptiveBitrateManager(
    min_bitrate=2000,
    max_bitrate=8000
)

# Adjust for network conditions
bitrate_manager.adjust_for_network(
    packet_loss=0.5,
    latency_ms=50
)
```

### Monitoring Optimization

```python
# Adjust check interval based on load
monitor = HealthMonitor(
    check_interval_seconds=30  # More frequent for critical systems
)

# Resolve old alerts
for alert in monitor.get_active_alerts():
    if alert.timestamp < datetime.now() - timedelta(hours=24):
        monitor.resolve_alert(alert.alert_id)
```

---

## 🐛 Troubleshooting

### Scheduler Issues

**Debates not running**
- Check schedule with `scheduler.get_schedule()`
- Verify callbacks are set
- Check for quiet hours configuration

**Too many/few debates**
- Adjust `interval_minutes`
- Check `max_debates_per_day`
- Review `quiet_hours` settings

### Streaming Issues

**Stream not connecting**
- Verify stream keys and RTMP URLs
- Check network connectivity
- Review firewall rules
- Enable fallback URLs

**Poor stream quality**
- Reduce bitrate/quality
- Check network bandwidth
- Monitor frame drop rate
- Enable adaptive bitrate

### Monitoring Issues

**Health checks failing**
- Verify check functions are registered
- Check service availability
- Review error messages in alerts
- Adjust check timeouts

---

## 📚 Architecture

```
automation/
├── scheduler.py        # Automated debate scheduling
├── streaming.py        # Multi-platform streaming
├── monitoring.py       # Health monitoring & alerts
├── analytics.py        # Metrics & analytics
├── __init__.py        # Package exports
└── README.md          # This file

examples/
└── automation_demo.py  # Comprehensive demo
```

**Key Classes**:
- `DebateScheduler` - Automated scheduling
- `MultiPlatformStreamer` - Stream management
- `HealthMonitor` - Health & alerting
- `AnalyticsDashboard` - Metrics & insights

**Data Flow**:
```
Schedule → Debate Trigger → Stream Start → Health Check
    ↓            ↓              ↓              ↓
Analytics ← Metrics ← Stream End ← Monitor
```

---

## ✅ Testing

Run the comprehensive demo:

```bash
python examples/automation_demo.py
```

Tests include:
- ✅ Automated scheduling (interval & adaptive)
- ✅ Multi-platform streaming
- ✅ Health monitoring with alerts
- ✅ Analytics dashboard
- ✅ Complete integration

---

**Phase 5.1 Complete** ✅

Automation & Scale provides production-ready infrastructure for 24/7 automated debate operation with enterprise-grade monitoring and analytics.

**Statistics**:
- **Total Code**: ~2,318 lines
- **Components**: 4 (Scheduler, Streaming, Monitoring, Analytics)
- **Platforms**: 5+ streaming platforms
- **Health Checks**: 8 predefined checks

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
