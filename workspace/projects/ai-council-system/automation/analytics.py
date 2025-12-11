"""
Analytics & Metrics System

Tracks comprehensive metrics and generates insights for automated debates.
Provides real-time and historical analytics for performance optimization.

Author: AI Council System
Phase: 5.1 - Automation & Scale
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from collections import defaultdict
import json
from pathlib import Path


@dataclass
class DebateMetrics:
    """Metrics for a single debate"""
    debate_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0.0
    topic: str = ""
    participant_count: int = 0
    round_count: int = 0
    total_responses: int = 0
    avg_response_length: float = 0.0
    avg_confidence: float = 0.0
    viewer_count_peak: int = 0
    engagement_score: float = 0.0
    consensus_level: float = 0.0
    controversy_score: float = 0.0

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "debate_id": self.debate_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "topic": self.topic,
            "participant_count": self.participant_count,
            "round_count": self.round_count,
            "total_responses": self.total_responses,
            "avg_response_length": self.avg_response_length,
            "avg_confidence": self.avg_confidence,
            "viewer_count_peak": self.viewer_count_peak,
            "engagement_score": self.engagement_score,
            "consensus_level": self.consensus_level,
            "controversy_score": self.controversy_score
        }


@dataclass
class StreamingMetrics:
    """Streaming performance metrics"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    platforms: List[str] = field(default_factory=list)
    total_viewers_peak: int = 0
    avg_bitrate_kbps: float = 0.0
    total_bytes_sent: int = 0
    uptime_percent: float = 100.0
    frame_drop_rate: float = 0.0

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "platforms": self.platforms,
            "total_viewers_peak": self.total_viewers_peak,
            "avg_bitrate_kbps": self.avg_bitrate_kbps,
            "total_bytes_sent": self.total_bytes_sent,
            "uptime_percent": self.uptime_percent,
            "frame_drop_rate": self.frame_drop_rate
        }


@dataclass
class SystemMetrics:
    """Overall system performance metrics"""
    timestamp: datetime
    cpu_usage_percent: float = 0.0
    memory_usage_percent: float = 0.0
    disk_usage_percent: float = 0.0
    network_in_mbps: float = 0.0
    network_out_mbps: float = 0.0
    active_debates: int = 0
    active_streams: int = 0

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "cpu_usage_percent": self.cpu_usage_percent,
            "memory_usage_percent": self.memory_usage_percent,
            "disk_usage_percent": self.disk_usage_percent,
            "network_in_mbps": self.network_in_mbps,
            "network_out_mbps": self.network_out_mbps,
            "active_debates": self.active_debates,
            "active_streams": self.active_streams
        }


class AnalyticsDashboard:
    """
    Analytics and metrics tracking system

    Features:
    - Debate performance tracking
    - Streaming metrics
    - System resource monitoring
    - Historical data storage
    - Trend analysis
    - Real-time dashboards
    """

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize analytics dashboard

        Args:
            data_dir: Directory for storing analytics data
        """
        self.data_dir = data_dir
        if data_dir:
            self.data_dir = Path(data_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)

        # Metrics storage
        self.debate_metrics: List[DebateMetrics] = []
        self.streaming_metrics: List[StreamingMetrics] = []
        self.system_metrics: List[SystemMetrics] = []

        # Aggregated statistics
        self.total_debates = 0
        self.total_stream_time_hours = 0.0
        self.total_viewers_all_time = 0

    def record_debate(self, metrics: DebateMetrics):
        """Record debate metrics"""
        self.debate_metrics.append(metrics)
        self.total_debates += 1

        # Save to disk if configured
        if self.data_dir:
            self._save_debate_metrics(metrics)

    def record_streaming(self, metrics: StreamingMetrics):
        """Record streaming metrics"""
        self.streaming_metrics.append(metrics)

        if metrics.end_time and metrics.start_time:
            duration_hours = (metrics.end_time - metrics.start_time).total_seconds() / 3600
            self.total_stream_time_hours += duration_hours

        # Save to disk if configured
        if self.data_dir:
            self._save_streaming_metrics(metrics)

    def record_system(self, metrics: SystemMetrics):
        """Record system metrics"""
        self.system_metrics.append(metrics)

        # Keep only recent system metrics (last 24 hours)
        cutoff = datetime.now() - timedelta(hours=24)
        self.system_metrics = [
            m for m in self.system_metrics
            if m.timestamp >= cutoff
        ]

    def get_debate_statistics(self, days: int = 7) -> Dict[str, Any]:
        """
        Get debate statistics for the last N days

        Args:
            days: Number of days to analyze

        Returns:
            Statistics dictionary
        """
        cutoff = datetime.now() - timedelta(days=days)
        recent_debates = [
            d for d in self.debate_metrics
            if d.start_time >= cutoff
        ]

        if not recent_debates:
            return {
                "total_debates": 0,
                "avg_duration_minutes": 0.0,
                "avg_participants": 0.0,
                "avg_engagement": 0.0
            }

        return {
            "total_debates": len(recent_debates),
            "avg_duration_minutes": sum(d.duration_seconds for d in recent_debates) / len(recent_debates) / 60,
            "avg_participants": sum(d.participant_count for d in recent_debates) / len(recent_debates),
            "avg_rounds": sum(d.round_count for d in recent_debates) / len(recent_debates),
            "avg_engagement": sum(d.engagement_score for d in recent_debates) / len(recent_debates),
            "avg_controversy": sum(d.controversy_score for d in recent_debates) / len(recent_debates),
            "avg_consensus": sum(d.consensus_level for d in recent_debates) / len(recent_debates),
            "peak_viewers": max((d.viewer_count_peak for d in recent_debates), default=0),
            "debates_per_day": len(recent_debates) / days
        }

    def get_streaming_statistics(self, days: int = 7) -> Dict[str, Any]:
        """Get streaming statistics"""
        cutoff = datetime.now() - timedelta(days=days)
        recent_streams = [
            s for s in self.streaming_metrics
            if s.start_time >= cutoff
        ]

        if not recent_streams:
            return {
                "total_streams": 0,
                "total_hours": 0.0,
                "avg_viewers": 0
            }

        total_hours = sum(
            (s.end_time - s.start_time).total_seconds() / 3600
            for s in recent_streams
            if s.end_time
        )

        return {
            "total_streams": len(recent_streams),
            "total_hours": total_hours,
            "avg_viewers": sum(s.total_viewers_peak for s in recent_streams) / len(recent_streams),
            "total_viewers_peak": max((s.total_viewers_peak for s in recent_streams), default=0),
            "avg_bitrate": sum(s.avg_bitrate_kbps for s in recent_streams) / len(recent_streams),
            "avg_uptime": sum(s.uptime_percent for s in recent_streams) / len(recent_streams),
            "platforms_used": list(set(
                platform
                for stream in recent_streams
                for platform in stream.platforms
            ))
        }

    def get_system_statistics(self) -> Dict[str, Any]:
        """Get current system statistics"""
        if not self.system_metrics:
            return {
                "avg_cpu": 0.0,
                "avg_memory": 0.0,
                "avg_disk": 0.0
            }

        recent = self.system_metrics[-100:]  # Last 100 samples

        return {
            "avg_cpu": sum(m.cpu_usage_percent for m in recent) / len(recent),
            "avg_memory": sum(m.memory_usage_percent for m in recent) / len(recent),
            "avg_disk": sum(m.disk_usage_percent for m in recent) / len(recent),
            "avg_network_in": sum(m.network_in_mbps for m in recent) / len(recent),
            "avg_network_out": sum(m.network_out_mbps for m in recent) / len(recent),
            "peak_cpu": max((m.cpu_usage_percent for m in recent), default=0.0),
            "peak_memory": max((m.memory_usage_percent for m in recent), default=0.0),
            "current_active_debates": recent[-1].active_debates if recent else 0,
            "current_active_streams": recent[-1].active_streams if recent else 0
        }

    def get_topic_trends(self, days: int = 30) -> Dict[str, int]:
        """Get trending debate topics"""
        cutoff = datetime.now() - timedelta(days=days)
        recent_debates = [
            d for d in self.debate_metrics
            if d.start_time >= cutoff and d.topic
        ]

        topic_counts = defaultdict(int)
        for debate in recent_debates:
            # Extract keywords from topic (simplified)
            words = debate.topic.lower().split()
            for word in words:
                if len(word) > 4:  # Only count significant words
                    topic_counts[word] += 1

        # Return top 10
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_topics[:10])

    def get_engagement_trends(self, days: int = 7) -> List[Dict]:
        """Get engagement trends over time"""
        cutoff = datetime.now() - timedelta(days=days)
        recent_debates = [
            d for d in self.debate_metrics
            if d.start_time >= cutoff
        ]

        # Group by day
        daily_engagement = defaultdict(list)
        for debate in recent_debates:
            day = debate.start_time.date()
            daily_engagement[day].append(debate.engagement_score)

        # Calculate daily averages
        trends = []
        for day in sorted(daily_engagement.keys()):
            scores = daily_engagement[day]
            trends.append({
                "date": day.isoformat(),
                "avg_engagement": sum(scores) / len(scores),
                "debate_count": len(scores)
            })

        return trends

    def get_performance_insights(self) -> Dict[str, Any]:
        """Generate performance insights and recommendations"""
        debate_stats = self.get_debate_statistics(days=7)
        streaming_stats = self.get_streaming_statistics(days=7)
        system_stats = self.get_system_statistics()

        insights = {
            "health": "good",
            "recommendations": [],
            "highlights": []
        }

        # Analyze debate performance
        if debate_stats["avg_engagement"] > 0.7:
            insights["highlights"].append("High engagement levels maintained")
        elif debate_stats["avg_engagement"] < 0.4:
            insights["recommendations"].append("Consider more controversial topics to boost engagement")

        # Analyze streaming performance
        if streaming_stats.get("avg_uptime", 100) < 95:
            insights["health"] = "needs_attention"
            insights["recommendations"].append("Streaming uptime below target (95%)")

        # Analyze system resources
        if system_stats["avg_cpu"] > 80:
            insights["health"] = "warning"
            insights["recommendations"].append("High CPU usage - consider scaling")

        if system_stats["avg_memory"] > 85:
            insights["recommendations"].append("High memory usage - check for leaks")

        # Success metrics
        if debate_stats["debates_per_day"] >= 10:
            insights["highlights"].append(f"Consistent output: {debate_stats['debates_per_day']:.1f} debates/day")

        if streaming_stats.get("total_viewers_peak", 0) > 1000:
            insights["highlights"].append(f"Peak viewership: {streaming_stats['total_viewers_peak']} concurrent viewers")

        return insights

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        return {
            "timestamp": datetime.now().isoformat(),
            "overview": {
                "total_debates_all_time": self.total_debates,
                "total_stream_hours": self.total_stream_time_hours,
                "total_viewers_all_time": self.total_viewers_all_time
            },
            "debates": self.get_debate_statistics(days=7),
            "streaming": self.get_streaming_statistics(days=7),
            "system": self.get_system_statistics(),
            "topic_trends": self.get_topic_trends(days=30),
            "engagement_trends": self.get_engagement_trends(days=7),
            "insights": self.get_performance_insights()
        }

    def _save_debate_metrics(self, metrics: DebateMetrics):
        """Save debate metrics to file"""
        if not self.data_dir:
            return

        date_str = metrics.start_time.strftime("%Y%m%d")
        file_path = self.data_dir / f"debates_{date_str}.jsonl"

        with open(file_path, 'a') as f:
            f.write(json.dumps(metrics.to_dict()) + "\n")

    def _save_streaming_metrics(self, metrics: StreamingMetrics):
        """Save streaming metrics to file"""
        if not self.data_dir:
            return

        date_str = metrics.start_time.strftime("%Y%m%d")
        file_path = self.data_dir / f"streaming_{date_str}.jsonl"

        with open(file_path, 'a') as f:
            f.write(json.dumps(metrics.to_dict()) + "\n")

    def export_report(self, output_path: Path, days: int = 30):
        """
        Export comprehensive analytics report

        Args:
            output_path: Where to save report
            days: Days of data to include
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "period_days": days,
            "debate_statistics": self.get_debate_statistics(days),
            "streaming_statistics": self.get_streaming_statistics(days),
            "system_statistics": self.get_system_statistics(),
            "topic_trends": self.get_topic_trends(days),
            "engagement_trends": self.get_engagement_trends(days),
            "insights": self.get_performance_insights()
        }

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📊 Analytics report exported to: {output_path}")
