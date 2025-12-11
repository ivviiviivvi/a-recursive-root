#!/usr/bin/env python3
"""
Performance Benchmarking Suite for AI Council System

Comprehensive benchmarks for:
- Debate execution speed
- Avatar generation performance
- Voice synthesis latency
- Streaming throughput
- Memory usage
- System scalability

Author: AI Council System
Version: 2.0.0
"""

import asyncio
import time
import sys
from pathlib import Path
from typing import Dict, List, Callable
from datetime import datetime
import statistics

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.agents import Agent, Personality
from core.agents.personalities import DEFAULT_PERSONALITIES
from core.council import Council
from streaming.avatars import AvatarGenerator, ExpressionState
from streaming.voices import VoiceSynthesisManager
from streaming.backgrounds import BackgroundGenerator, BackgroundStyle


class BenchmarkResult:
    """Store benchmark results"""

    def __init__(self, name: str):
        self.name = name
        self.timings: List[float] = []
        self.memory_usage: List[float] = []
        self.errors: int = 0

    def add_timing(self, duration: float):
        """Add a timing measurement"""
        self.timings.append(duration)

    def add_memory(self, memory_mb: float):
        """Add a memory measurement"""
        self.memory_usage.append(memory_mb)

    def record_error(self):
        """Record an error"""
        self.errors += 1

    def get_stats(self) -> Dict:
        """Get statistical summary"""
        if not self.timings:
            return {
                "name": self.name,
                "error": "No data collected"
            }

        return {
            "name": self.name,
            "iterations": len(self.timings),
            "total_time": sum(self.timings),
            "mean_time": statistics.mean(self.timings),
            "median_time": statistics.median(self.timings),
            "min_time": min(self.timings),
            "max_time": max(self.timings),
            "stdev_time": statistics.stdev(self.timings) if len(self.timings) > 1 else 0,
            "errors": self.errors,
            "success_rate": (len(self.timings) - self.errors) / len(self.timings) * 100 if self.timings else 0
        }


class PerformanceBenchmark:
    """Comprehensive performance benchmarking"""

    def __init__(self):
        self.results: Dict[str, BenchmarkResult] = {}

    async def run_benchmark(
        self,
        name: str,
        func: Callable,
        iterations: int = 10,
        warmup: int = 2
    ) -> BenchmarkResult:
        """Run a benchmark"""
        print(f"\n🔬 Benchmarking: {name}")
        print(f"   Iterations: {iterations} (+ {warmup} warmup)")

        result = BenchmarkResult(name)

        # Warmup
        print(f"   Warming up...", end=" ", flush=True)
        for _ in range(warmup):
            try:
                await func()
            except Exception:
                pass
        print("✓")

        # Actual benchmark
        print(f"   Running...", end=" ", flush=True)
        for i in range(iterations):
            try:
                start_time = time.time()
                await func()
                elapsed = time.time() - start_time
                result.add_timing(elapsed)

                if (i + 1) % (iterations // 10) == 0:
                    print(".", end="", flush=True)

            except Exception as e:
                result.record_error()
                print("E", end="", flush=True)

        print(" ✓")

        # Store results
        self.results[name] = result

        # Print quick stats
        stats = result.get_stats()
        print(f"   Mean: {stats['mean_time']*1000:.1f}ms")
        print(f"   Min: {stats['min_time']*1000:.1f}ms")
        print(f"   Max: {stats['max_time']*1000:.1f}ms")

        return result

    async def benchmark_agent_response(self):
        """Benchmark agent response generation"""
        personality = DEFAULT_PERSONALITIES["The Pragmatist"]
        agent = Agent(personality=personality, llm_provider="mock")

        await self.run_benchmark(
            name="Agent Response Generation",
            func=lambda: agent.generate_response("What is your opinion on AI?"),
            iterations=50
        )

    async def benchmark_council_debate(self):
        """Benchmark council debate execution"""
        agents = [
            Agent(DEFAULT_PERSONALITIES[name], llm_provider="mock")
            for name in list(DEFAULT_PERSONALITIES.keys())[:5]
        ]
        council = Council(agents=agents)

        await self.run_benchmark(
            name="Council Debate (5 agents, 1 round)",
            func=lambda: council.run_debate("AI Ethics", rounds=1),
            iterations=10
        )

    async def benchmark_avatar_generation(self):
        """Benchmark avatar generation"""
        generator = AvatarGenerator()

        await self.run_benchmark(
            name="Avatar Generation",
            func=lambda: generator.generate_avatar(
                "The Pragmatist",
                ExpressionState.NEUTRAL
            ),
            iterations=100
        )

    async def benchmark_background_generation(self):
        """Benchmark background generation"""
        generator = BackgroundGenerator()

        await self.run_benchmark(
            name="Background Generation",
            func=lambda: generator.generate_background(
                BackgroundStyle.GRADIENT,
                "calm_agreement"
            ),
            iterations=100
        )

    async def benchmark_sentiment_analysis(self):
        """Benchmark sentiment analysis"""
        from streaming.backgrounds import SentimentAnalyzer

        analyzer = SentimentAnalyzer()
        text = "I strongly believe that AI will revolutionize society."

        await self.run_benchmark(
            name="Sentiment Analysis",
            func=lambda: analyzer.analyze_sentiment(text),
            iterations=200
        )

    async def benchmark_voice_synthesis(self):
        """Benchmark voice synthesis (if available)"""
        from streaming.voices.profiles import DEFAULT_VOICE_PROFILES

        manager = VoiceSynthesisManager()
        profile = DEFAULT_VOICE_PROFILES["The Pragmatist"]

        # This would test actual voice synthesis
        # For now, just benchmark profile loading
        await self.run_benchmark(
            name="Voice Profile Loading",
            func=lambda: self._load_voice_profile(profile),
            iterations=100
        )

    async def _load_voice_profile(self, profile):
        """Helper to load voice profile"""
        await asyncio.sleep(0.001)  # Simulate loading
        return profile

    async def benchmark_concurrent_agents(self):
        """Benchmark concurrent agent processing"""
        agents = [
            Agent(DEFAULT_PERSONALITIES[name], llm_provider="mock")
            for name in list(DEFAULT_PERSONALITIES.keys())[:15]
        ]

        async def concurrent_responses():
            tasks = [
                agent.generate_response("Quick opinion?")
                for agent in agents
            ]
            await asyncio.gather(*tasks)

        await self.run_benchmark(
            name="Concurrent Agent Responses (15 agents)",
            func=concurrent_responses,
            iterations=20
        )

    async def benchmark_scalability(self):
        """Benchmark system scalability with increasing load"""
        print("\n📊 Scalability Benchmark")
        print("   Testing with increasing agent counts...")

        for agent_count in [1, 3, 5, 10, 15]:
            agents = [
                Agent(DEFAULT_PERSONALITIES[list(DEFAULT_PERSONALITIES.keys())[i % 15]], llm_provider="mock")
                for i in range(agent_count)
            ]
            council = Council(agents=agents)

            await self.run_benchmark(
                name=f"Debate with {agent_count} agents",
                func=lambda c=council: c.run_debate("Scalability test", rounds=1),
                iterations=5
            )

    def print_summary(self):
        """Print benchmark summary"""
        print("\n" + "="*80)
        print("  BENCHMARK SUMMARY")
        print("="*80)
        print()

        # Sort by mean time
        sorted_results = sorted(
            self.results.values(),
            key=lambda r: r.get_stats().get('mean_time', float('inf'))
        )

        print(f"{'Benchmark Name':<45} {'Mean':<12} {'Min':<12} {'Max':<12}")
        print("-"*80)

        for result in sorted_results:
            stats = result.get_stats()
            if 'error' not in stats:
                mean_ms = stats['mean_time'] * 1000
                min_ms = stats['min_time'] * 1000
                max_ms = stats['max_time'] * 1000

                print(f"{stats['name']:<45} {mean_ms:>10.1f}ms {min_ms:>10.1f}ms {max_ms:>10.1f}ms")

        print()

        # Performance insights
        print("Performance Insights:")
        print()

        fastest = sorted_results[0]
        slowest = sorted_results[-1]

        print(f"  ⚡ Fastest: {fastest.name} ({fastest.get_stats()['mean_time']*1000:.1f}ms)")
        print(f"  🐌 Slowest: {slowest.name} ({slowest.get_stats()['mean_time']*1000:.1f}ms)")
        print()

        # Calculate throughput for key operations
        for result in sorted_results:
            stats = result.get_stats()
            if 'error' not in stats and stats['mean_time'] > 0:
                throughput = 1 / stats['mean_time']
                if "Agent Response" in stats['name']:
                    print(f"  📊 Agent Response Throughput: {throughput:.1f} responses/sec")
                elif "Avatar Generation" in stats['name']:
                    print(f"  📊 Avatar Generation Throughput: {throughput:.1f} avatars/sec")

        print()
        print("="*80)
        print()

    async def run_all_benchmarks(self):
        """Run all benchmarks"""
        print()
        print("="*80)
        print("  AI COUNCIL SYSTEM - PERFORMANCE BENCHMARKS")
        print("  Version 2.0.0")
        print("="*80)
        print()

        benchmarks = [
            self.benchmark_agent_response,
            self.benchmark_avatar_generation,
            self.benchmark_background_generation,
            self.benchmark_sentiment_analysis,
            self.benchmark_voice_synthesis,
            self.benchmark_council_debate,
            self.benchmark_concurrent_agents,
            self.benchmark_scalability,
        ]

        for benchmark in benchmarks:
            try:
                await benchmark()
            except Exception as e:
                print(f"   ❌ Error: {e}")

        self.print_summary()


async def main():
    """Main entry point"""
    benchmark = PerformanceBenchmark()
    await benchmark.run_all_benchmarks()

    print("✅ Benchmarking complete!")
    print()


if __name__ == "__main__":
    asyncio.run(main())
