"""
Automated Debate Scheduler

Orchestrates 24/7 automated debate operation with intelligent scheduling,
event monitoring, and automatic debate triggering.

Author: AI Council System
Phase: 5.1 - Automation & Scale
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict, Callable, Any
import asyncio
from pathlib import Path
import json


class ScheduleType(Enum):
    """Types of debate scheduling"""
    INTERVAL = "interval"        # Fixed time intervals
    CRON = "cron"               # Cron-like schedule
    EVENT_DRIVEN = "event"      # Triggered by events
    ADAPTIVE = "adaptive"       # AI-determined optimal times


class DebateStatus(Enum):
    """Status of scheduled debate"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ScheduleConfig:
    """Configuration for debate scheduling"""
    schedule_type: ScheduleType = ScheduleType.INTERVAL
    interval_minutes: int = 60
    cron_expression: Optional[str] = None
    min_interval_minutes: int = 30
    max_debates_per_day: int = 24
    quiet_hours_start: int = 2  # 2 AM
    quiet_hours_end: int = 6    # 6 AM
    adaptive_mode: bool = True
    require_trending_topic: bool = False


@dataclass
class ScheduledDebate:
    """A scheduled debate"""
    debate_id: str
    scheduled_time: datetime
    topic: Optional[str] = None
    status: DebateStatus = DebateStatus.PENDING
    actual_start_time: Optional[datetime] = None
    actual_end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "debate_id": self.debate_id,
            "scheduled_time": self.scheduled_time.isoformat(),
            "topic": self.topic,
            "status": self.status.value,
            "actual_start_time": self.actual_start_time.isoformat() if self.actual_start_time else None,
            "actual_end_time": self.actual_end_time.isoformat() if self.actual_end_time else None,
            "error_message": self.error_message,
            "metadata": self.metadata
        }


class DebateScheduler:
    """
    Automated debate scheduler for 24/7 operation

    Features:
    - Multiple scheduling strategies
    - Intelligent timing (avoid quiet hours)
    - Event-driven triggering
    - Debate queue management
    - Error recovery
    - Statistics tracking
    """

    def __init__(self, config: ScheduleConfig):
        """
        Initialize debate scheduler

        Args:
            config: Schedule configuration
        """
        self.config = config
        self.schedule: List[ScheduledDebate] = []
        self.current_debate: Optional[ScheduledDebate] = None
        self.running = False

        # Callbacks
        self.on_debate_start: Optional[Callable] = None
        self.on_debate_complete: Optional[Callable] = None
        self.on_debate_error: Optional[Callable] = None

        # Statistics
        self.total_debates_scheduled = 0
        self.total_debates_completed = 0
        self.total_debates_failed = 0

    def set_callbacks(
        self,
        on_start: Optional[Callable] = None,
        on_complete: Optional[Callable] = None,
        on_error: Optional[Callable] = None
    ):
        """Set callback functions for debate lifecycle"""
        self.on_debate_start = on_start
        self.on_debate_complete = on_complete
        self.on_debate_error = on_error

    def schedule_debate(
        self,
        scheduled_time: datetime,
        topic: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> ScheduledDebate:
        """
        Schedule a new debate

        Args:
            scheduled_time: When to run the debate
            topic: Optional debate topic
            metadata: Optional metadata

        Returns:
            ScheduledDebate object
        """
        debate_id = f"debate_{int(scheduled_time.timestamp())}"

        debate = ScheduledDebate(
            debate_id=debate_id,
            scheduled_time=scheduled_time,
            topic=topic,
            metadata=metadata or {}
        )

        self.schedule.append(debate)
        self.total_debates_scheduled += 1

        # Sort schedule by time
        self.schedule.sort(key=lambda d: d.scheduled_time)

        return debate

    def generate_schedule(
        self,
        start_time: datetime,
        duration_hours: int = 24
    ) -> List[ScheduledDebate]:
        """
        Generate debate schedule for a time period

        Args:
            start_time: Start of schedule period
            duration_hours: Duration in hours

        Returns:
            List of scheduled debates
        """
        end_time = start_time + timedelta(hours=duration_hours)
        current_time = start_time
        scheduled = []

        if self.config.schedule_type == ScheduleType.INTERVAL:
            # Fixed interval scheduling
            while current_time < end_time:
                # Skip quiet hours
                if self._is_quiet_hour(current_time):
                    current_time += timedelta(hours=1)
                    continue

                # Check max debates per day
                debates_today = self._count_debates_on_date(current_time.date())
                if debates_today >= self.config.max_debates_per_day:
                    current_time += timedelta(days=1)
                    current_time = current_time.replace(hour=self.config.quiet_hours_end)
                    continue

                debate = self.schedule_debate(current_time)
                scheduled.append(debate)

                current_time += timedelta(minutes=self.config.interval_minutes)

        elif self.config.schedule_type == ScheduleType.ADAPTIVE:
            # Adaptive scheduling based on optimal times
            optimal_hours = [9, 12, 15, 18, 21]  # Peak engagement times

            for day in range(duration_hours // 24 + 1):
                day_start = start_time + timedelta(days=day)

                for hour in optimal_hours:
                    schedule_time = day_start.replace(hour=hour, minute=0, second=0)

                    if schedule_time < start_time or schedule_time > end_time:
                        continue

                    debate = self.schedule_debate(schedule_time)
                    scheduled.append(debate)

        return scheduled

    def _is_quiet_hour(self, time: datetime) -> bool:
        """Check if time is within quiet hours"""
        hour = time.hour

        if self.config.quiet_hours_start < self.config.quiet_hours_end:
            return self.config.quiet_hours_start <= hour < self.config.quiet_hours_end
        else:
            # Quiet hours span midnight
            return hour >= self.config.quiet_hours_start or hour < self.config.quiet_hours_end

    def _count_debates_on_date(self, date) -> int:
        """Count debates scheduled on a specific date"""
        return sum(
            1 for debate in self.schedule
            if debate.scheduled_time.date() == date
        )

    def get_next_debate(self) -> Optional[ScheduledDebate]:
        """Get the next pending debate"""
        now = datetime.now()

        for debate in self.schedule:
            if debate.status == DebateStatus.PENDING and debate.scheduled_time <= now:
                return debate

        return None

    def cancel_debate(self, debate_id: str) -> bool:
        """Cancel a scheduled debate"""
        for debate in self.schedule:
            if debate.debate_id == debate_id and debate.status == DebateStatus.PENDING:
                debate.status = DebateStatus.CANCELLED
                return True
        return False

    async def run_debate(self, debate: ScheduledDebate) -> bool:
        """
        Execute a scheduled debate

        Args:
            debate: Debate to run

        Returns:
            True if successful
        """
        debate.status = DebateStatus.RUNNING
        debate.actual_start_time = datetime.now()
        self.current_debate = debate

        try:
            # Call start callback
            if self.on_debate_start:
                await self.on_debate_start(debate)

            # Simulate debate execution (in production, call actual debate system)
            # This is where you'd integrate with:
            # - Event ingestion
            # - Topic extraction
            # - Council formation
            # - Debate execution
            # - Video generation
            # - Streaming

            await asyncio.sleep(2)  # Simulated debate time

            # Mark complete
            debate.status = DebateStatus.COMPLETED
            debate.actual_end_time = datetime.now()
            self.total_debates_completed += 1

            # Call complete callback
            if self.on_debate_complete:
                await self.on_debate_complete(debate)

            return True

        except Exception as e:
            debate.status = DebateStatus.FAILED
            debate.error_message = str(e)
            debate.actual_end_time = datetime.now()
            self.total_debates_failed += 1

            # Call error callback
            if self.on_debate_error:
                await self.on_debate_error(debate, e)

            return False

        finally:
            self.current_debate = None

    async def start(self):
        """Start the automated scheduler"""
        self.running = True
        print(f"🤖 Debate Scheduler started")

        while self.running:
            # Check for next debate
            next_debate = self.get_next_debate()

            if next_debate:
                print(f"▶️  Starting debate: {next_debate.debate_id}")
                await self.run_debate(next_debate)

                # Wait minimum interval before next debate
                await asyncio.sleep(self.config.min_interval_minutes * 60)
            else:
                # No pending debates, wait and check again
                await asyncio.sleep(60)

                # Auto-generate next debate if adaptive mode
                if self.config.adaptive_mode:
                    self._auto_schedule_next()

    def _auto_schedule_next(self):
        """Automatically schedule next debate"""
        # Check if we need to schedule more debates
        pending_count = sum(
            1 for d in self.schedule
            if d.status == DebateStatus.PENDING
        )

        if pending_count < 3:  # Keep at least 3 debates queued
            next_time = datetime.now() + timedelta(minutes=self.config.interval_minutes)

            # Adjust for quiet hours
            while self._is_quiet_hour(next_time):
                next_time += timedelta(hours=1)

            self.schedule_debate(next_time)

    async def stop(self):
        """Stop the scheduler"""
        self.running = False
        print(f"🛑 Debate Scheduler stopped")

    def get_schedule(
        self,
        status: Optional[DebateStatus] = None,
        limit: Optional[int] = None
    ) -> List[ScheduledDebate]:
        """
        Get scheduled debates

        Args:
            status: Filter by status
            limit: Maximum number to return

        Returns:
            List of debates
        """
        debates = self.schedule

        if status:
            debates = [d for d in debates if d.status == status]

        if limit:
            debates = debates[:limit]

        return debates

    def get_statistics(self) -> Dict:
        """Get scheduler statistics"""
        pending = sum(1 for d in self.schedule if d.status == DebateStatus.PENDING)
        running = sum(1 for d in self.schedule if d.status == DebateStatus.RUNNING)
        completed = sum(1 for d in self.schedule if d.status == DebateStatus.COMPLETED)
        failed = sum(1 for d in self.schedule if d.status == DebateStatus.FAILED)
        cancelled = sum(1 for d in self.schedule if d.status == DebateStatus.CANCELLED)

        return {
            "total_scheduled": self.total_debates_scheduled,
            "total_completed": self.total_debates_completed,
            "total_failed": self.total_debates_failed,
            "pending": pending,
            "running": running,
            "completed": completed,
            "failed": failed,
            "cancelled": cancelled,
            "success_rate": (completed / max(1, completed + failed)) * 100,
            "current_debate": self.current_debate.debate_id if self.current_debate else None,
            "next_debate_time": self.get_next_debate().scheduled_time.isoformat() if self.get_next_debate() else None
        }

    def save_schedule(self, path: Path):
        """Save schedule to file"""
        data = {
            "config": {
                "schedule_type": self.config.schedule_type.value,
                "interval_minutes": self.config.interval_minutes,
                "max_debates_per_day": self.config.max_debates_per_day
            },
            "debates": [d.to_dict() for d in self.schedule],
            "statistics": self.get_statistics()
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def clear_completed(self):
        """Remove completed/failed/cancelled debates from schedule"""
        self.schedule = [
            d for d in self.schedule
            if d.status in [DebateStatus.PENDING, DebateStatus.RUNNING]
        ]


class EventTriggeredScheduler(DebateScheduler):
    """
    Event-driven debate scheduler

    Triggers debates based on external events (trending topics, news, etc.)
    """

    def __init__(self, config: ScheduleConfig):
        super().__init__(config)
        self.event_threshold = 0.7  # Controversy threshold to trigger debate

    async def monitor_events(self):
        """Monitor events and trigger debates"""
        while self.running:
            # Check for high-controversy events
            # In production, integrate with event ingestion system
            await asyncio.sleep(300)  # Check every 5 minutes

            # Simulate event detection
            if self.config.require_trending_topic:
                # Would call actual event system here
                pass

    def trigger_debate_from_event(self, event_data: Dict) -> ScheduledDebate:
        """
        Trigger immediate debate from event

        Args:
            event_data: Event information

        Returns:
            Scheduled debate
        """
        # Schedule for immediate execution
        scheduled_time = datetime.now() + timedelta(minutes=5)

        topic = event_data.get("topic", "Current Event")

        return self.schedule_debate(
            scheduled_time=scheduled_time,
            topic=topic,
            metadata={"event_triggered": True, "event_data": event_data}
        )
