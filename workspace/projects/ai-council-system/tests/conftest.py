"""
Pytest configuration and shared fixtures for AI Council System tests

Author: AI Council System
Version: 2.0.0
"""

import pytest
import asyncio
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Core components
from core.agents import Agent, Personality
from core.agents.personalities import DEFAULT_PERSONALITIES
from core.council import Council
from core.events import Event, EventIngestor

# Blockchain
from blockchain.token import TokenManager
from blockchain.rng import HybridRNG

# Streaming
from streaming.avatars import AvatarGenerator
from streaming.voices import VoiceSynthesisManager
from streaming.backgrounds import BackgroundGenerator

# Automation
from automation import (
    AutomationOrchestrator,
    OrchestratorConfig,
    OrchestratorMode,
    HealthMonitor,
    AnalyticsDashboard
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_personality():
    """Provide a sample personality for testing"""
    return Personality(
        name="Test Agent",
        description="A test agent for unit testing",
        debate_style="Analytical and methodical",
        core_values=["accuracy", "thoroughness"],
        expertise_areas=["testing", "quality assurance"],
        communication_style="Clear and precise",
        bias_tendencies=["confirmation bias"],
        typical_arguments=["Evidence-based reasoning"],
        interaction_patterns={"formal": 0.8, "collaborative": 0.7}
    )


@pytest.fixture
def sample_agent(sample_personality):
    """Provide a sample agent for testing"""
    return Agent(
        personality=sample_personality,
        llm_provider="mock"
    )


@pytest.fixture
def sample_council(sample_agent):
    """Provide a sample council for testing"""
    agents = [sample_agent for _ in range(3)]
    return Council(agents=agents)


@pytest.fixture
def sample_event():
    """Provide a sample event for testing"""
    return Event(
        source="twitter",
        content="Test event content for debate topic extraction",
        timestamp=datetime.now(),
        metadata={"test": True}
    )


@pytest.fixture
def token_manager():
    """Provide token manager for testing"""
    return TokenManager()


@pytest.fixture
def hybrid_rng():
    """Provide RNG for testing"""
    return HybridRNG()


@pytest.fixture
def avatar_generator():
    """Provide avatar generator for testing"""
    return AvatarGenerator()


@pytest.fixture
def voice_manager():
    """Provide voice manager for testing"""
    return VoiceSynthesisManager()


@pytest.fixture
def background_generator():
    """Provide background generator for testing"""
    return BackgroundGenerator()


@pytest.fixture
async def health_monitor():
    """Provide health monitor for testing"""
    return HealthMonitor()


@pytest.fixture
def analytics_dashboard():
    """Provide analytics dashboard for testing"""
    return AnalyticsDashboard()


@pytest.fixture
async def orchestrator():
    """Provide orchestrator for testing"""
    config = OrchestratorConfig(
        mode=OrchestratorMode.TEST,
        enable_streaming=False,
        enable_health_monitoring=True,
        enable_analytics=True
    )
    orch = AutomationOrchestrator(config)
    await orch.initialize()
    return orch


@pytest.fixture
def temp_cache_dir(tmp_path):
    """Provide temporary cache directory"""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return cache_dir


@pytest.fixture
def temp_recording_dir(tmp_path):
    """Provide temporary recording directory"""
    recording_dir = tmp_path / "recordings"
    recording_dir.mkdir()
    return recording_dir


# Mock data fixtures
@pytest.fixture
def mock_debate_data():
    """Provide mock debate data"""
    return {
        "debate_id": "test_debate_001",
        "topic": "The Future of AI Testing",
        "scheduled_time": datetime.now(),
        "agent_count": 5,
        "round_count": 3,
        "status": "pending"
    }


@pytest.fixture
def mock_streaming_config():
    """Provide mock streaming configuration"""
    return {
        "platforms": ["youtube", "twitch"],
        "quality": "high",
        "record": True,
        "bitrate_kbps": 5000
    }


@pytest.fixture
def mock_health_checks():
    """Provide mock health check results"""
    return {
        "scheduler": {"status": "healthy", "response_time_ms": 10},
        "streaming": {"status": "healthy", "response_time_ms": 15},
        "database": {"status": "healthy", "response_time_ms": 5},
        "disk_space": {"status": "healthy", "response_time_ms": 2}
    }
