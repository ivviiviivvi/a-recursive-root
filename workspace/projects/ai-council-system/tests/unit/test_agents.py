"""
Unit tests for AI agents and personalities

Author: AI Council System
Version: 2.0.0
"""

import pytest
from core.agents import Agent, Personality
from core.agents.personalities import DEFAULT_PERSONALITIES


class TestPersonality:
    """Test Personality class"""

    def test_personality_creation(self, sample_personality):
        """Test creating a personality"""
        assert sample_personality.name == "Test Agent"
        assert "testing" in sample_personality.expertise_areas
        assert len(sample_personality.core_values) > 0

    def test_default_personalities_exist(self):
        """Test that default personalities are loaded"""
        assert len(DEFAULT_PERSONALITIES) == 15
        assert "The Pragmatist" in DEFAULT_PERSONALITIES
        assert "The Visionary" in DEFAULT_PERSONALITIES

    def test_personality_attributes(self):
        """Test personality has required attributes"""
        personality = DEFAULT_PERSONALITIES["The Pragmatist"]
        assert hasattr(personality, 'name')
        assert hasattr(personality, 'debate_style')
        assert hasattr(personality, 'expertise_areas')
        assert hasattr(personality, 'core_values')


class TestAgent:
    """Test Agent class"""

    def test_agent_creation(self, sample_agent):
        """Test creating an agent"""
        assert sample_agent is not None
        assert sample_agent.personality.name == "Test Agent"

    def test_agent_with_different_providers(self, sample_personality):
        """Test agent creation with different LLM providers"""
        providers = ["mock", "anthropic", "openai", "ollama"]
        for provider in providers:
            agent = Agent(personality=sample_personality, llm_provider=provider)
            assert agent is not None

    @pytest.mark.asyncio
    async def test_agent_generate_response(self, sample_agent):
        """Test agent can generate a response"""
        prompt = "What is your opinion on testing?"
        response = await sample_agent.generate_response(prompt)
        assert response is not None
        assert len(response) > 0

    def test_agent_personality_preservation(self, sample_agent):
        """Test agent preserves personality traits"""
        assert sample_agent.personality.name == "Test Agent"
        assert "testing" in sample_agent.personality.expertise_areas


class TestMemory:
    """Test agent memory system"""

    @pytest.mark.asyncio
    async def test_agent_remembers_context(self, sample_agent):
        """Test agent memory retention"""
        # First interaction
        response1 = await sample_agent.generate_response("Remember: my name is Alice")

        # Second interaction - should remember
        response2 = await sample_agent.generate_response("What is my name?")

        # Memory should be maintained
        assert len(sample_agent.memory) >= 2

    def test_memory_limit(self, sample_agent):
        """Test memory has limits"""
        # Add many items to memory
        for i in range(100):
            sample_agent.memory.append(f"Item {i}")

        # Memory should not grow infinitely
        assert len(sample_agent.memory) <= sample_agent.max_memory_items


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
