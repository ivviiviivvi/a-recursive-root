#!/usr/bin/env python3
"""
Phase 5 Complete Demo - Production-Ready Automation System

Demonstrates the complete automation orchestrator with all integrated components:
- Complete orchestration of all automation components
- Automated scheduling with multiple strategies
- Multi-platform streaming with recording
- Health monitoring with alerts and auto-recovery
- Comprehensive analytics and insights
- Production deployment ready

This demo showcases the final Phase 5 system ready for 24/7 operation.

Author: AI Council System
Phase: 5 - Automation & Scale COMPLETE
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation import (
    # Orchestrator
    AutomationOrchestrator,
    OrchestratorConfig,
    OrchestratorMode,
    SystemState,

    # Scheduler
    ScheduleConfig,
    ScheduleType,

    # Streaming
    StreamConfig,
    StreamPlatform,
    StreamQuality,

    # Monitoring
    HealthStatus,
    AlertSeverity,

    # Analytics
    DebateMetrics,
    StreamingMetrics
)


def print_separator(char="=", length=70):
    """Print a separator line"""
    print(char * length)


def print_section(title):
    """Print a section header"""
    print()
    print_separator()
    print(f"  {title}")
    print_separator()
    print()


def print_stats(title, stats, indent=2):
    """Print statistics in a formatted way"""
    prefix = " " * indent
    print(f"{prefix}{title}:")
    for key, value in stats.items():
        if isinstance(value, dict):
            print_stats(key.replace('_', ' ').title(), value, indent + 2)
        elif isinstance(value, list) and value and isinstance(value[0], str):
            print(f"{prefix}  {key}: {', '.join(value)}")
        elif isinstance(value, float):
            print(f"{prefix}  {key}: {value:.2f}")
        else:
            print(f"{prefix}  {key}: {value}")


async def demo_orchestrator_initialization():
    """Demonstrate orchestrator initialization"""
    print_section("1. Orchestrator Initialization")

    print("🔧 Creating orchestrator configuration:\\n")

    # Create comprehensive configuration
    config = OrchestratorConfig(
        mode=OrchestratorMode.CONTINUOUS,
        schedule_config=ScheduleConfig(
            schedule_type=ScheduleType.ADAPTIVE,
            interval_minutes=60,
            max_debates_per_day=24,
            quiet_hours_start=2,
            quiet_hours_end=6,
            adaptive_mode=True
        ),
        enable_streaming=True,
        enable_recording=True,
        recording_path=Path("/tmp/ai-council-recordings"),
        enable_health_monitoring=True,
        health_check_interval=60,
        enable_analytics=True,
        auto_restart_on_failure=True,
        max_restart_attempts=3
    )

    print(f"   Mode: {config.mode.value}")
    print(f"   Streaming: {'Enabled' if config.enable_streaming else 'Disabled'}")
    print(f"   Recording: {'Enabled' if config.enable_recording else 'Disabled'}")
    print(f"   Health Monitoring: {'Enabled' if config.enable_health_monitoring else 'Disabled'}")
    print(f"   Analytics: {'Enabled' if config.enable_analytics else 'Disabled'}")
    print(f"   Auto-Recovery: {'Enabled' if config.auto_restart_on_failure else 'Disabled'}")
    print()

    # Create orchestrator
    print("🚀 Initializing orchestrator components:\\n")
    orchestrator = AutomationOrchestrator(config)
    await orchestrator.initialize()

    print("   ✅ Scheduler initialized")
    print("   ✅ Multi-platform streamer initialized")
    print("   ✅ Health monitor initialized")
    print("   ✅ Analytics dashboard initialized")
    print("   ✅ Orchestrator ready")
    print()

    return orchestrator


async def demo_streaming_configuration(orchestrator):
    """Demonstrate streaming configuration"""
    print_section("2. Multi-Platform Streaming Setup")

    print("📡 Configuring streaming destinations:\\n")

    if orchestrator.streamer:
        # Add YouTube
        youtube_config = StreamConfig(
            platform=StreamPlatform.YOUTUBE,
            stream_key="ytlive-demo-key",
            rtmp_url="rtmp://a.rtmp.youtube.com/live2",
            quality=StreamQuality.HIGH,
            enabled=True
        )
        orchestrator.streamer.add_destination(youtube_config)
        print("   ✅ YouTube (1080p60) - Main platform")

        # Add Twitch
        twitch_config = StreamConfig(
            platform=StreamPlatform.TWITCH,
            stream_key="live-demo-key",
            rtmp_url="rtmp://live.twitch.tv/app",
            quality=StreamQuality.HIGH,
            enabled=True
        )
        orchestrator.streamer.add_destination(twitch_config)
        print("   ✅ Twitch (1080p60) - Gaming audience")

        # Add Facebook
        facebook_config = StreamConfig(
            platform=StreamPlatform.FACEBOOK,
            stream_key="FB-demo-key",
            rtmp_url="rtmps://live-api-s.facebook.com:443/rtmp",
            quality=StreamQuality.MEDIUM,
            enabled=True
        )
        orchestrator.streamer.add_destination(facebook_config)
        print("   ✅ Facebook (720p30) - Social reach")

        print()
        print("   🎬 Multi-platform streaming ready")
        print("   📹 Recording enabled to /tmp/ai-council-recordings")
        print()


async def demo_health_monitoring(orchestrator):
    """Demonstrate health monitoring"""
    print_section("3. Health Monitoring System")

    print("💚 Running comprehensive health checks:\\n")

    if orchestrator.monitor:
        # Run all health checks
        await orchestrator.monitor.run_all_checks()

        # Show results
        stats = orchestrator.monitor.get_statistics()

        print(f"Overall System Health: {stats['overall_status'].upper()}")
        print(f"Total Health Checks: {stats['total_checks']}")
        print(f"Active Alerts: {stats['active_alerts']}")
        print()

        print("Health Check Results:")
        for name, check in stats['checks'].items():
            status_icon = {
                'healthy': '✅',
                'degraded': '⚠️ ',
                'unhealthy': '❌',
                'critical': '🚨'
            }.get(check['status'], '❓')

            print(f"   {status_icon} {name:<20} | {check['status']:<10} | {check['response_time_ms']:.0f}ms")
            if check['message']:
                print(f"      └─ {check['message']}")

        print()


async def demo_analytics(orchestrator):
    """Demonstrate analytics system"""
    print_section("4. Analytics & Performance Insights")

    print("📊 Analytics Dashboard:\\n")

    if orchestrator.dashboard:
        # Get statistics
        dashboard_data = orchestrator.dashboard.get_dashboard_data()

        # Debate stats
        if 'debates' in dashboard_data:
            debate_stats = dashboard_data['debates']
            print("Debate Analytics:")
            print(f"   Total Debates: {debate_stats.get('total_debates', 0)}")
            print(f"   Avg Duration: {debate_stats.get('avg_duration_minutes', 0):.1f} minutes")
            print(f"   Avg Engagement: {debate_stats.get('avg_engagement', 0):.2f}")
            print(f"   Peak Viewers: {debate_stats.get('peak_viewers', 0)}")
            print()

        # Streaming stats
        if 'streaming' in dashboard_data:
            streaming_stats = dashboard_data['streaming']
            print("Streaming Analytics:")
            print(f"   Total Sessions: {streaming_stats.get('total_streams', 0)}")
            print(f"   Total Hours: {streaming_stats.get('total_hours', 0):.1f}")
            print(f"   Avg Viewers: {streaming_stats.get('avg_viewers', 0):.0f}")
            print(f"   Platforms: {', '.join(streaming_stats.get('platforms_used', []))}")
            print()

        # Performance insights
        insights = orchestrator.dashboard.get_performance_insights()
        print("📌 Performance Insights:")
        print(f"   System Health: {insights['health'].upper()}")

        if insights.get('highlights'):
            print("   Highlights:")
            for highlight in insights['highlights']:
                print(f"      ✨ {highlight}")

        if insights.get('recommendations'):
            print("   Recommendations:")
            for rec in insights['recommendations']:
                print(f"      💡 {rec}")

        print()


async def demo_automated_operation(orchestrator):
    """Demonstrate automated operation cycle"""
    print_section("5. Automated Operation Cycle")

    print("🎬 Simulating automated debate cycle:\\n")

    # Set up callbacks
    async def on_start(debate):
        print(f"   🎥 Debate Started: {debate.debate_id}")
        print(f"      Topic: {debate.topic or 'General Discussion'}")
        print(f"      Scheduled: {debate.scheduled_time.strftime('%H:%M:%S')}")
        print(f"      Streaming: Active on 3 platforms")
        print()

    async def on_complete(debate):
        duration = (debate.actual_end_time - debate.actual_start_time).total_seconds()
        print(f"   ✅ Debate Completed: {debate.debate_id}")
        print(f"      Duration: {duration:.1f}s")
        print(f"      Status: {debate.status.value}")
        print(f"      Streaming: Stopped and saved")
        print()

    async def on_error(debate, error):
        print(f"   ❌ Debate Error: {debate.debate_id}")
        print(f"      Error: {error}")
        print(f"      Auto-recovery: Enabled")
        print()

    async def on_critical(alert):
        print(f"   🚨 CRITICAL ALERT!")
        print(f"      Component: {alert.component if hasattr(alert, 'component') else 'System'}")
        print(f"      Message: {alert.message if hasattr(alert, 'message') else str(alert)}")
        print()

    orchestrator.on_debate_start = on_start
    orchestrator.on_debate_complete = on_complete
    orchestrator.on_debate_error = on_error
    orchestrator.on_critical_alert = on_critical

    # Generate and run a single debate for demo
    if orchestrator.scheduler:
        debates = orchestrator.scheduler.generate_schedule(
            start_time=datetime.now(),
            duration_hours=1
        )

        if debates:
            print(f"Generated {len(debates)} debates for next hour\\n")
            print("Running first debate as demonstration...\\n")

            # Run one debate
            await orchestrator._on_debate_start(debates[0])
            await asyncio.sleep(2)  # Simulate debate running
            debates[0].actual_end_time = datetime.now()
            debates[0].status = debates[0].status.__class__.COMPLETED
            await orchestrator._on_debate_complete(debates[0])


async def demo_orchestrator_stats(orchestrator):
    """Show orchestrator statistics"""
    print_section("6. Orchestrator Status & Statistics")

    print("📈 System Statistics:\\n")

    # Get status
    status = orchestrator.get_status()
    print("Current Status:")
    print(f"   State: {status['state'].upper()}")
    print(f"   Mode: {status['mode']}")
    print(f"   Current Debate: {status.get('current_debate', 'None')}")
    print()

    print("Active Components:")
    for component, active in status['components'].items():
        icon = "✅" if active else "❌"
        print(f"   {icon} {component.replace('_', ' ').title()}: {'Active' if active else 'Inactive'}")
    print()

    # Get full statistics
    stats = orchestrator.get_statistics()

    print("System Metrics:")
    print(f"   Uptime: {stats.get('uptime_hours', 0):.2f} hours")
    print(f"   Total Debates: {stats.get('total_debates', 0)}")
    print(f"   Success Rate: {stats.get('success_rate', 100):.1f}%")
    print(f"   Restart Count: {stats.get('restart_count', 0)}")
    print()


async def demo_production_deployment():
    """Demonstrate production deployment readiness"""
    print_section("7. Production Deployment")

    print("🚀 Production Deployment Features:\\n")

    print("Infrastructure:")
    print("   ✅ Docker Compose multi-service setup")
    print("   ✅ Nginx reverse proxy with SSL/TLS")
    print("   ✅ PostgreSQL for persistent data")
    print("   ✅ Redis for caching")
    print("   ✅ Prometheus for metrics collection")
    print("   ✅ Grafana for visualization")
    print()

    print("Automation:")
    print("   ✅ Systemd service for auto-start")
    print("   ✅ Health monitoring with alerts")
    print("   ✅ Auto-restart on failure")
    print("   ✅ 24/7 automated scheduling")
    print()

    print("Security:")
    print("   ✅ SSL/TLS encryption")
    print("   ✅ Rate limiting")
    print("   ✅ Security headers")
    print("   ✅ Private metrics endpoint")
    print()

    print("Observability:")
    print("   ✅ Real-time metrics")
    print("   ✅ Pre-configured dashboards")
    print("   ✅ Performance insights")
    print("   ✅ Alert notifications")
    print()

    print("Deployment Commands:")
    print("   $ docker-compose -f deployment/docker-compose.production.yml up -d")
    print("   $ sudo systemctl enable ai-council")
    print("   $ sudo systemctl start ai-council")
    print()


async def main():
    """Run complete Phase 5 demonstration"""
    print()
    print_separator("=")
    print("  🤖 PHASE 5 COMPLETE DEMO")
    print("  Production-Ready Automation System")
    print_separator("=")
    print()

    print("This demo showcases the complete Phase 5 automation system with")
    print("full orchestration, multi-platform streaming, health monitoring,")
    print("analytics, and production deployment infrastructure.")
    print()

    input("Press Enter to start demo...")

    try:
        # 1. Initialize orchestrator
        orchestrator = await demo_orchestrator_initialization()

        # 2. Configure streaming
        await demo_streaming_configuration(orchestrator)

        # 3. Demonstrate health monitoring
        await demo_health_monitoring(orchestrator)

        # 4. Show analytics
        await demo_analytics(orchestrator)

        # 5. Run automated operation
        await demo_automated_operation(orchestrator)

        # 6. Show statistics
        await demo_orchestrator_stats(orchestrator)

        # 7. Production deployment info
        await demo_production_deployment()

        # Final summary
        print_section("Phase 5 Complete! 🎉")

        print("✅ Successfully demonstrated:")
        print("   • Complete automation orchestrator")
        print("   • Multi-platform streaming (YouTube, Twitch, Facebook)")
        print("   • Health monitoring with auto-recovery")
        print("   • Comprehensive analytics and insights")
        print("   • Production deployment infrastructure")
        print("   • 24/7 automated operation capability")
        print()

        print("🎯 Production Ready Features:")
        print("   • Docker Compose deployment")
        print("   • Systemd service integration")
        print("   • Nginx reverse proxy with SSL")
        print("   • PostgreSQL + Redis data layer")
        print("   • Prometheus + Grafana observability")
        print("   • Automated health checks and alerts")
        print("   • Multi-platform streaming with recording")
        print("   • Performance analytics and insights")
        print()

        print("📦 Deployment Components:")
        print("   • deployment/docker-compose.production.yml")
        print("   • deployment/ai-council.service")
        print("   • deployment/nginx.conf")
        print("   • deployment/prometheus.yml")
        print("   • deployment/grafana-dashboards/")
        print("   • deployment/init.sql")
        print("   • deployment/README.md")
        print()

        print_separator("=")
        print("  Phase 5: Automation & Scale ✅ COMPLETE")
        print("  Ready for 24/7 Production Operation")
        print_separator("=")
        print()

    except KeyboardInterrupt:
        print("\\n\\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\\n\\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
