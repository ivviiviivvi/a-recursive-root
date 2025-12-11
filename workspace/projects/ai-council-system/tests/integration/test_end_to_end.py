"""
Integration tests for end-to-end workflows

Author: AI Council System
Version: 2.0.0
"""

import pytest
import asyncio
from datetime import datetime


class TestDebateWorkflow:
    """Test complete debate workflow"""

    @pytest.mark.asyncio
    async def test_full_debate_cycle(self, sample_council, mock_debate_data):
        """Test complete debate from start to finish"""
        # Create debate
        debate_id = mock_debate_data["debate_id"]
        topic = mock_debate_data["topic"]

        # Run debate (simplified)
        result = await sample_council.run_debate(
            topic=topic,
            rounds=mock_debate_data["round_count"]
        )

        assert result is not None
        assert "rounds" in result
        assert len(result["rounds"]) == mock_debate_data["round_count"]

    @pytest.mark.asyncio
    async def test_agent_participation(self, sample_council):
        """Test all agents participate in debate"""
        result = await sample_council.run_debate(
            topic="Test topic",
            rounds=2
        )

        # Each agent should have contributed
        for round_data in result["rounds"]:
            assert len(round_data["responses"]) == len(sample_council.agents)


class TestEventToDebatePipeline:
    """Test event ingestion to debate execution"""

    @pytest.mark.asyncio
    async def test_event_to_topic_extraction(self, sample_event):
        """Test extracting topic from event"""
        from core.events import TopicExtractor

        extractor = TopicExtractor()
        topics = extractor.extract_topics(sample_event)

        assert len(topics) > 0
        assert all("topic" in t for t in topics)
        assert all("relevance" in t for t in topics)

    @pytest.mark.asyncio
    async def test_full_event_pipeline(self, sample_event, sample_council):
        """Test complete event to debate pipeline"""
        from core.events import TopicExtractor

        # Extract topic
        extractor = TopicExtractor()
        topics = extractor.extract_topics(sample_event)

        if topics:
            selected_topic = topics[0]["topic"]

            # Run debate on extracted topic
            result = await sample_council.run_debate(
                topic=selected_topic,
                rounds=2
            )

            assert result is not None


class TestMediaProductionPipeline:
    """Test media production integration"""

    @pytest.mark.asyncio
    async def test_avatar_generation(self, avatar_generator):
        """Test avatar generation for debate"""
        from streaming.avatars import ExpressionState

        avatar = avatar_generator.generate_avatar(
            personality_name="The Pragmatist",
            expression=ExpressionState.NEUTRAL
        )

        assert avatar is not None

    @pytest.mark.asyncio
    async def test_voice_synthesis(self, voice_manager):
        """Test voice synthesis pipeline"""
        from streaming.voices.profiles import DEFAULT_VOICE_PROFILES

        profile = DEFAULT_VOICE_PROFILES["The Pragmatist"]
        # Voice synthesis would be tested here
        assert profile is not None

    @pytest.mark.asyncio
    async def test_complete_media_pipeline(self, avatar_generator, background_generator):
        """Test complete media production"""
        from streaming.avatars import ExpressionState
        from streaming.backgrounds import BackgroundStyle

        # Generate avatar
        avatar = avatar_generator.generate_avatar(
            personality_name="The Pragmatist",
            expression=ExpressionState.SPEAKING
        )

        # Generate background
        background = background_generator.generate_background(
            style=BackgroundStyle.GRADIENT,
            mood="calm_agreement"
        )

        assert avatar is not None
        assert background is not None


class TestAutomationIntegration:
    """Test automation system integration"""

    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initializes all components"""
        assert orchestrator.scheduler is not None
        assert orchestrator.monitor is not None
        assert orchestrator.dashboard is not None

    @pytest.mark.asyncio
    async def test_health_monitoring(self, orchestrator):
        """Test health monitoring integration"""
        await orchestrator.monitor.run_all_checks()
        stats = orchestrator.monitor.get_statistics()

        assert "overall_status" in stats
        assert "checks" in stats

    @pytest.mark.asyncio
    async def test_analytics_collection(self, orchestrator):
        """Test analytics data collection"""
        dashboard_data = orchestrator.dashboard.get_dashboard_data()

        assert dashboard_data is not None
        assert isinstance(dashboard_data, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
