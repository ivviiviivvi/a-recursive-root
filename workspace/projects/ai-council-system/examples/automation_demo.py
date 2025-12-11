#!/usr/bin/env python3
"""
Automation & Scale Demo

Demonstrates 24/7 automated operation with scheduling, multi-platform streaming,
health monitoring, and analytics.

Author: AI Council System
Phase: 5.1 - Automation & Scale
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from automation import (
    # Scheduler
    DebateScheduler,
    ScheduleConfig,
    ScheduleType,
    DebateStatus,

    # Streaming
    MultiPlatformStreamer,
    StreamConfig,
    StreamPlatform,
    StreamQuality,
    StreamRecorder,

    # Monitoring
    HealthMonitor,
    check_scheduler_health,
    check_streaming_health,
    check_disk_space,
    check_memory_usage,

    # Analytics
    AnalyticsDashboard,
    DebateMetrics,
    StreamingMetrics,
    SystemMetrics
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


async def demo_scheduler():
    """Demonstrate debate scheduler"""
    print_section("1. Automated Debate Scheduler")

    # Create scheduler config
    config = ScheduleConfig(
        schedule_type=ScheduleType.INTERVAL,
        interval_minutes=30,
        max_debates_per_day=24,
        quiet_hours_start=2,
        quiet_hours_end=6,
        adaptive_mode=True
    )

    scheduler = DebateScheduler(config)

    print("🗓️  Generating 24-hour debate schedule:\n")

    # Generate schedule for next 24 hours
    start_time = datetime.now()
    debates = scheduler.generate_schedule(start_time, duration_hours=24)

    print(f"Generated {len(debates)} debates:")
    for i, debate in enumerate(debates[:10], 1):  # Show first 10
        print(f"   {i}. {debate.scheduled_time.strftime('%Y-%m-%d %H:%M')} - {debate.debate_id}")

    if len(debates) > 10:
        print(f"   ... and {len(debates) - 10} more")

    print()

    # Show statistics
    stats = scheduler.get_statistics()
    print("📊 Scheduler Statistics:")
    print(f"   Total Scheduled: {stats['total_scheduled']}")
    print(f"   Pending: {stats['pending']}")
    print(f"   Next Debate: {stats['next_debate_time']}")
    print()

    # Simulate running a debate
    print("▶️  Simulating debate execution:")

    async def on_start(debate):
        print(f"   🎬 Starting: {debate.debate_id}")

    async def on_complete(debate):
        print(f"   ✅ Completed: {debate.debate_id} (duration: {(debate.actual_end_time - debate.actual_start_time).total_seconds():.1f}s)")

    scheduler.set_callbacks(on_start=on_start, on_complete=on_complete)

    # Run first debate
    if debates:
        await scheduler.run_debate(debates[0])

    print()


async def demo_streaming():
    """Demonstrate multi-platform streaming"""
    print_section("2. Multi-Platform Streaming")

    streamer = MultiPlatformStreamer()

    print("📡 Configuring streaming destinations:\n")

    # Add YouTube
    youtube_config = StreamConfig(
        platform=StreamPlatform.YOUTUBE,
        stream_key="ytlive-mock-key",
        rtmp_url="rtmp://a.rtmp.youtube.com/live2",
        quality=StreamQuality.HIGH,
        enabled=True
    )
    streamer.add_destination(youtube_config)
    print("   ✅ YouTube configured (1080p)")

    # Add Twitch
    twitch_config = StreamConfig(
        platform=StreamPlatform.TWITCH,
        stream_key="live_mock_key",
        rtmp_url="rtmp://live.twitch.tv/app",
        quality=StreamQuality.HIGH,
        enabled=True
    )
    streamer.add_destination(twitch_config)
    print("   ✅ Twitch configured (1080p)")

    # Add Facebook
    facebook_config = StreamConfig(
        platform=StreamPlatform.FACEBOOK,
        stream_key="FB-mock-key",
        rtmp_url="rtmps://live-api-s.facebook.com:443/rtmp",
        quality=StreamQuality.MEDIUM,
        enabled=True
    )
    streamer.add_destination(facebook_config)
    print("   ✅ Facebook configured (720p)")

    print()

    # Start streaming
    print("📤 Starting multi-platform stream:")
    await streamer.start_streaming()

    # Simulate streaming for a bit
    await asyncio.sleep(3)

    # Show metrics
    print()
    stats = streamer.get_statistics()
    print("📊 Streaming Statistics:")
    print(f"   Live Destinations: {stats['live_destinations']}/{stats['total_destinations']}")
    print(f"   Total Viewers: {stats['total_viewers']}")
    print(f"   Average Bitrate: {stats['average_bitrate_kbps']:.0f} kbps")
    print()

    for platform, metrics in stats['destinations'].items():
        status_icon = "🟢" if metrics['status'] == 'live' else "🔴"
        print(f"   {status_icon} {platform.upper():<10} | {metrics['fps']:.0f} FPS | {metrics['bitrate_kbps']:.0f} kbps | Drops: {metrics['drop_rate_percent']:.2f}%")

    print()

    # Stop streaming
    print("🛑 Stopping streams...")
    await streamer.stop_streaming()

    print()


async def demo_monitoring():
    """Demonstrate health monitoring"""
    print_section("3. Health Monitoring & Alerts")

    monitor = HealthMonitor(check_interval_seconds=5)

    print("💚 Registering health checks:\n")

    # Register health checks
    monitor.register_check("scheduler", check_scheduler_health)
    monitor.register_check("streaming", check_streaming_health)
    monitor.register_check("disk_space", check_disk_space)
    monitor.register_check("memory", check_memory_usage)

    print("   ✓ Scheduler health check")
    print("   ✓ Streaming health check")
    print("   ✓ Disk space check")
    print("   ✓ Memory usage check")
    print()

    # Alert callback
    async def on_alert(alert):
        severity_icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "critical": "🚨"
        }
        icon = severity_icons.get(alert.severity.value, "")
        print(f"   {icon} [{alert.severity.value.upper()}] {alert.component}: {alert.message}")

    monitor.on_alert = on_alert

    # Run health checks
    print("🔍 Running health checks:")
    await monitor.run_all_checks()

    print()

    # Show results
    stats = monitor.get_statistics()
    print(f"Overall Status: {stats['overall_status'].upper()}")
    print(f"Total Checks: {stats['total_checks']}")
    print(f"Active Alerts: {stats['active_alerts']}")
    print()

    print("Health Check Results:")
    for name, check in stats['checks'].items():
        status_icon = "✅" if check['status'] == 'healthy' else "❌"
        print(f"   {status_icon} {name:<15} | {check['message']} ({check['response_time_ms']:.0f}ms)")

    print()


async def demo_analytics():
    """Demonstrate analytics dashboard"""
    print_section("4. Analytics & Metrics")

    dashboard = AnalyticsDashboard()

    print("📈 Recording sample debate metrics:\n")

    # Record sample debates
    for i in range(5):
        metrics = DebateMetrics(
            debate_id=f"debate_{i+1}",
            start_time=datetime.now() - timedelta(hours=i),
            end_time=datetime.now() - timedelta(hours=i, minutes=-25),
            duration_seconds=1500 + (i * 100),
            topic=f"Sample Topic {i+1}",
            participant_count=5,
            round_count=3,
            total_responses=15,
            avg_response_length=150 + (i * 10),
            avg_confidence=0.75 + (i * 0.02),
            viewer_count_peak=100 + (i * 50),
            engagement_score=0.65 + (i * 0.05),
            consensus_level=0.70 - (i * 0.05),
            controversy_score=0.30 + (i * 0.08)
        )
        dashboard.record_debate(metrics)
        print(f"   ✓ Recorded: {metrics.topic} (engagement: {metrics.engagement_score:.2f})")

    print()

    # Record streaming metrics
    streaming = StreamingMetrics(
        session_id="stream_1",
        start_time=datetime.now() - timedelta(hours=2),
        end_time=datetime.now(),
        platforms=["youtube", "twitch", "facebook"],
        total_viewers_peak=350,
        avg_bitrate_kbps=6000,
        total_bytes_sent=5_000_000_000,
        uptime_percent=98.5,
        frame_drop_rate=0.8
    )
    dashboard.record_streaming(streaming)

    print("📊 Analytics Dashboard:\n")

    # Get statistics
    debate_stats = dashboard.get_debate_statistics(days=7)
    streaming_stats = dashboard.get_streaming_statistics(days=7)

    print("Debate Statistics (Last 7 Days):")
    print(f"   Total Debates: {debate_stats['total_debates']}")
    print(f"   Avg Duration: {debate_stats['avg_duration_minutes']:.1f} minutes")
    print(f"   Avg Participants: {debate_stats['avg_participants']:.1f}")
    print(f"   Avg Engagement: {debate_stats['avg_engagement']:.2f}")
    print(f"   Peak Viewers: {debate_stats['peak_viewers']}")
    print(f"   Debates/Day: {debate_stats['debates_per_day']:.1f}")
    print()

    print("Streaming Statistics (Last 7 Days):")
    print(f"   Total Streams: {streaming_stats['total_streams']}")
    print(f"   Total Hours: {streaming_stats['total_hours']:.1f}")
    print(f"   Avg Viewers: {streaming_stats['avg_viewers']:.0f}")
    print(f"   Avg Bitrate: {streaming_stats['avg_bitrate']:.0f} kbps")
    print(f"   Avg Uptime: {streaming_stats['avg_uptime']:.1f}%")
    print(f"   Platforms: {', '.join(streaming_stats['platforms_used'])}")
    print()

    # Get insights
    insights = dashboard.get_performance_insights()
    print("📌 Performance Insights:")
    print(f"   Health: {insights['health'].upper()}")

    if insights['highlights']:
        print("   Highlights:")
        for highlight in insights['highlights']:
            print(f"      ✨ {highlight}")

    if insights['recommendations']:
        print("   Recommendations:")
        for rec in insights['recommendations']:
            print(f"      💡 {rec}")

    print()


async def demo_integration():
    """Demonstrate integrated automation system"""
    print_section("5. Integrated Automation System")

    print("🚀 Initializing complete automation system:\n")

    # Initialize all components
    scheduler = DebateScheduler(ScheduleConfig(
        schedule_type=ScheduleType.ADAPTIVE,
        interval_minutes=60
    ))

    streamer = MultiPlatformStreamer()
    streamer.add_destination(StreamConfig(
        platform=StreamPlatform.YOUTUBE,
        stream_key="mock-key",
        rtmp_url="rtmp://mock.youtube.com/live",
        quality=StreamQuality.HIGH
    ))

    monitor = HealthMonitor(check_interval_seconds=10)
    monitor.register_check("scheduler", check_scheduler_health)
    monitor.register_check("streaming", check_streaming_health)

    dashboard = AnalyticsDashboard()

    print("   ✅ Scheduler initialized")
    print("   ✅ Streaming initialized")
    print("   ✅ Monitoring initialized")
    print("   ✅ Analytics initialized")
    print()

    print("📅 Generating schedule for next 12 hours:")
    debates = scheduler.generate_schedule(datetime.now(), duration_hours=12)
    print(f"   Scheduled {len(debates)} debates")
    print()

    print("🎬 Simulating automated operation:")

    # Simulate one complete cycle
    if debates:
        debate = debates[0]

        # 1. Health check before debate
        print("   1️⃣  Running pre-debate health checks...")
        await monitor.run_all_checks()
        overall_status = monitor.get_overall_status()
        print(f"      System health: {overall_status.value}")

        # 2. Start streaming
        print("   2️⃣  Starting multi-platform stream...")
        await streamer.start_streaming()
        print("      Stream live on YouTube")

        # 3. Run debate
        print("   3️⃣  Running debate...")
        await scheduler.run_debate(debate)
        print("      Debate completed successfully")

        # 4. Record metrics
        print("   4️⃣  Recording analytics...")
        metrics = DebateMetrics(
            debate_id=debate.debate_id,
            start_time=debate.actual_start_time,
            end_time=debate.actual_end_time,
            duration_seconds=2.0,
            topic="Automated Debate Example",
            participant_count=5,
            round_count=2,
            engagement_score=0.82,
            viewer_count_peak=250
        )
        dashboard.record_debate(metrics)
        print("      Metrics recorded")

        # 5. Stop streaming
        print("   5️⃣  Stopping stream...")
        await streamer.stop_streaming()
        print("      Stream ended")

        # 6. Generate report
        print("   6️⃣  Generating performance report...")
        report_stats = dashboard.get_dashboard_data()
        print(f"      Total debates: {report_stats['debates']['total_debates']}")
        print(f"      Avg engagement: {report_stats['debates']['avg_engagement']:.2f}")

    print()
    print("✅ Automated cycle complete!")
    print()


async def main():
    """Run all demos"""
    print()
    print_separator("=")
    print("  🤖 AUTOMATION & SCALE DEMO")
    print("  24/7 Automated Debate Operation")
    print_separator("=")
    print()

    print("This demo showcases the complete automation system for")
    print("continuous 24/7 debate operation with multi-platform streaming,")
    print("health monitoring, and comprehensive analytics.")
    print()

    input("Press Enter to start demo...")

    try:
        # Run demos
        await demo_scheduler()
        await demo_streaming()
        await demo_monitoring()
        await demo_analytics()
        await demo_integration()

        # Final summary
        print_section("Demo Complete!")

        print("✅ Successfully demonstrated:")
        print("   • Automated debate scheduling (interval & adaptive)")
        print("   • Multi-platform streaming (YouTube, Twitch, Facebook)")
        print("   • Health monitoring with alerts")
        print("   • Analytics dashboard with insights")
        print("   • Complete integrated automation")
        print()

        print("🎬 The automation system is ready for:")
        print("   • 24/7 continuous operation")
        print("   • Multi-platform distribution")
        print("   • Automated health monitoring")
        print("   • Real-time performance analytics")
        print("   • Production deployment")
        print()

        print_separator("=")
        print("  Phase 5.1: Automation & Scale ✅ COMPLETE")
        print_separator("=")
        print()

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
