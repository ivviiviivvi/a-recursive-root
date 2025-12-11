"""
Automation & Scale System

Provides 24/7 automated operation for AI Council debates with
multi-platform streaming, health monitoring, analytics, and complete
orchestration for production deployment.

Author: AI Council System
Phase: 5 - Automation & Scale COMPLETE
Version: 2.0.0
"""

# Scheduler
from .scheduler import (
    ScheduleType,
    DebateStatus,
    ScheduleConfig,
    ScheduledDebate,
    DebateScheduler,
    EventTriggeredScheduler
)

# Streaming
from .streaming import (
    StreamPlatform,
    StreamStatus,
    StreamQuality,
    StreamConfig,
    StreamMetrics,
    StreamDestination,
    MultiPlatformStreamer,
    AdaptiveBitrateManager,
    StreamRecorder
)

# Monitoring
from .monitoring import (
    HealthStatus,
    AlertSeverity,
    HealthCheck,
    Alert,
    HealthMonitor,
    check_scheduler_health,
    check_streaming_health,
    check_database_health,
    check_disk_space,
    check_memory_usage,
    check_api_endpoints,
    check_event_ingestion,
    check_tts_availability
)

# Analytics
from .analytics import (
    DebateMetrics,
    StreamingMetrics,
    SystemMetrics,
    AnalyticsDashboard
)

# Orchestrator
from .orchestrator import (
    OrchestratorMode,
    SystemState,
    OrchestratorConfig,
    OrchestratorStats,
    AutomationOrchestrator
)

__all__ = [
    # Scheduler
    "ScheduleType",
    "DebateStatus",
    "ScheduleConfig",
    "ScheduledDebate",
    "DebateScheduler",
    "EventTriggeredScheduler",

    # Streaming
    "StreamPlatform",
    "StreamStatus",
    "StreamQuality",
    "StreamConfig",
    "StreamMetrics",
    "StreamDestination",
    "MultiPlatformStreamer",
    "AdaptiveBitrateManager",
    "StreamRecorder",

    # Monitoring
    "HealthStatus",
    "AlertSeverity",
    "HealthCheck",
    "Alert",
    "HealthMonitor",
    "check_scheduler_health",
    "check_streaming_health",
    "check_database_health",
    "check_disk_space",
    "check_memory_usage",
    "check_api_endpoints",
    "check_event_ingestion",
    "check_tts_availability",

    # Analytics
    "DebateMetrics",
    "StreamingMetrics",
    "SystemMetrics",
    "AnalyticsDashboard",

    # Orchestrator
    "OrchestratorMode",
    "SystemState",
    "OrchestratorConfig",
    "OrchestratorStats",
    "AutomationOrchestrator",
]

__version__ = "2.0.0"
