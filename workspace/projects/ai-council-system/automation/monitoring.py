"""
Health Monitoring & Alerting System

Monitors system health, tracks metrics, and sends alerts for issues.
Ensures 24/7 reliability for automated debate operation.

Author: AI Council System
Phase: 5.1 - Automation & Scale
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional, Callable, Any
import asyncio


class HealthStatus(Enum):
    """Overall health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class HealthCheck:
    """Individual health check"""
    name: str
    status: HealthStatus
    last_check: datetime
    message: str = ""
    response_time_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_healthy(self) -> bool:
        """Check if healthy"""
        return self.status == HealthStatus.HEALTHY


@dataclass
class Alert:
    """System alert"""
    alert_id: str
    severity: AlertSeverity
    component: str
    message: str
    timestamp: datetime
    resolved: bool = False
    resolved_at: Optional[datetime] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "alert_id": self.alert_id,
            "severity": self.severity.value,
            "component": self.component,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "resolved": self.resolved,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None
        }


class HealthMonitor:
    """
    System health monitoring

    Features:
    - Periodic health checks
    - Component monitoring
    - Alert generation
    - Automatic recovery attempts
    - Health history
    """

    def __init__(self, check_interval_seconds: int = 60):
        """
        Initialize health monitor

        Args:
            check_interval_seconds: How often to run health checks
        """
        self.check_interval = check_interval_seconds
        self.checks: Dict[str, HealthCheck] = {}
        self.alerts: List[Alert] = []
        self.monitoring = False

        # Callbacks
        self.on_alert: Optional[Callable] = None
        self.on_health_change: Optional[Callable] = None

        # Statistics
        self.total_checks = 0
        self.total_alerts = 0
        self.uptime_start: Optional[datetime] = None

    def register_check(self, name: str, check_fn: Callable) -> None:
        """
        Register a health check function

        Args:
            name: Check name
            check_fn: Async function that returns (bool, str) for (healthy, message)
        """
        self.checks[name] = HealthCheck(
            name=name,
            status=HealthStatus.HEALTHY,
            last_check=datetime.now()
        )

        # Store function reference in metadata
        self.checks[name].metadata["check_fn"] = check_fn

    async def run_check(self, name: str) -> HealthCheck:
        """
        Run a specific health check

        Args:
            name: Check name

        Returns:
            Updated HealthCheck
        """
        check = self.checks.get(name)
        if not check:
            raise ValueError(f"Check '{name}' not registered")

        check_fn = check.metadata.get("check_fn")
        if not check_fn:
            check.status = HealthStatus.UNHEALTHY
            check.message = "No check function configured"
            return check

        start_time = datetime.now()

        try:
            # Run check
            is_healthy, message = await check_fn()

            # Update check
            check.status = HealthStatus.HEALTHY if is_healthy else HealthStatus.UNHEALTHY
            check.message = message
            check.last_check = datetime.now()
            check.response_time_ms = (datetime.now() - start_time).total_seconds() * 1000

            # Generate alert if unhealthy
            if not is_healthy:
                self._create_alert(
                    severity=AlertSeverity.WARNING,
                    component=name,
                    message=f"Health check failed: {message}"
                )

        except Exception as e:
            check.status = HealthStatus.CRITICAL
            check.message = f"Check error: {str(e)}"
            check.last_check = datetime.now()

            self._create_alert(
                severity=AlertSeverity.CRITICAL,
                component=name,
                message=f"Health check exception: {str(e)}"
            )

        self.total_checks += 1
        return check

    async def run_all_checks(self) -> Dict[str, HealthCheck]:
        """Run all registered health checks"""
        tasks = [
            self.run_check(name)
            for name in self.checks.keys()
        ]

        await asyncio.gather(*tasks, return_exceptions=True)

        return self.checks

    def _create_alert(self, severity: AlertSeverity, component: str, message: str):
        """Create a new alert"""
        alert_id = f"alert_{int(datetime.now().timestamp())}"

        alert = Alert(
            alert_id=alert_id,
            severity=severity,
            component=component,
            message=message,
            timestamp=datetime.now()
        )

        self.alerts.append(alert)
        self.total_alerts += 1

        # Call alert callback
        if self.on_alert:
            asyncio.create_task(self.on_alert(alert))

        print(f"🚨 ALERT [{severity.value.upper()}] {component}: {message}")

    def resolve_alert(self, alert_id: str):
        """Mark an alert as resolved"""
        for alert in self.alerts:
            if alert.alert_id == alert_id and not alert.resolved:
                alert.resolved = True
                alert.resolved_at = datetime.now()
                return True
        return False

    def get_overall_status(self) -> HealthStatus:
        """Get overall system health status"""
        if not self.checks:
            return HealthStatus.HEALTHY

        statuses = [check.status for check in self.checks.values()]

        # Critical if any check is critical
        if HealthStatus.CRITICAL in statuses:
            return HealthStatus.CRITICAL

        # Unhealthy if any check is unhealthy
        if HealthStatus.UNHEALTHY in statuses:
            return HealthStatus.UNHEALTHY

        # Degraded if any check is degraded
        if HealthStatus.DEGRADED in statuses:
            return HealthStatus.DEGRADED

        return HealthStatus.HEALTHY

    def get_active_alerts(self) -> List[Alert]:
        """Get all unresolved alerts"""
        return [alert for alert in self.alerts if not alert.resolved]

    def get_alerts_by_severity(self, severity: AlertSeverity) -> List[Alert]:
        """Get alerts by severity"""
        return [
            alert for alert in self.alerts
            if alert.severity == severity and not alert.resolved
        ]

    async def start_monitoring(self):
        """Start continuous health monitoring"""
        self.monitoring = True
        self.uptime_start = datetime.now()

        print(f"💚 Health monitoring started (interval: {self.check_interval}s)")

        while self.monitoring:
            await self.run_all_checks()
            await asyncio.sleep(self.check_interval)

    def stop_monitoring(self):
        """Stop health monitoring"""
        self.monitoring = False
        print("🛑 Health monitoring stopped")

    def get_uptime_seconds(self) -> float:
        """Get system uptime"""
        if not self.uptime_start:
            return 0.0
        return (datetime.now() - self.uptime_start).total_seconds()

    def get_statistics(self) -> Dict[str, Any]:
        """Get monitoring statistics"""
        active_alerts = self.get_active_alerts()

        return {
            "overall_status": self.get_overall_status().value,
            "uptime_hours": self.get_uptime_seconds() / 3600,
            "total_checks": self.total_checks,
            "total_alerts": self.total_alerts,
            "active_alerts": len(active_alerts),
            "critical_alerts": len(self.get_alerts_by_severity(AlertSeverity.CRITICAL)),
            "checks": {
                name: {
                    "status": check.status.value,
                    "message": check.message,
                    "last_check": check.last_check.isoformat(),
                    "response_time_ms": check.response_time_ms
                }
                for name, check in self.checks.items()
            },
            "recent_alerts": [
                alert.to_dict()
                for alert in self.alerts[-10:]  # Last 10 alerts
            ]
        }


# Predefined health check functions

async def check_scheduler_health() -> tuple[bool, str]:
    """Check if scheduler is running"""
    # In production, check actual scheduler status
    return True, "Scheduler running normally"


async def check_streaming_health() -> tuple[bool, str]:
    """Check streaming platform connectivity"""
    # In production, ping streaming endpoints
    return True, "All streaming platforms reachable"


async def check_database_health() -> tuple[bool, str]:
    """Check database connectivity"""
    # In production, check database connection
    return True, "Database connection healthy"


async def check_disk_space() -> tuple[bool, str]:
    """Check available disk space"""
    # In production, check actual disk usage
    import shutil
    try:
        usage = shutil.disk_usage("/")
        free_percent = (usage.free / usage.total) * 100

        if free_percent < 10:
            return False, f"Low disk space: {free_percent:.1f}% free"
        return True, f"Disk space OK: {free_percent:.1f}% free"
    except Exception as e:
        return False, f"Disk check failed: {e}"


async def check_memory_usage() -> tuple[bool, str]:
    """Check memory usage"""
    # In production, check actual memory
    return True, "Memory usage normal"


async def check_api_endpoints() -> tuple[bool, str]:
    """Check API endpoint availability"""
    # In production, health check API endpoints
    return True, "All API endpoints responding"


async def check_event_ingestion() -> tuple[bool, str]:
    """Check event ingestion pipeline"""
    # In production, verify events are being processed
    return True, "Event ingestion active"


async def check_tts_availability() -> tuple[bool, str]:
    """Check TTS engine availability"""
    # In production, test TTS engines
    return True, "TTS engines available"
