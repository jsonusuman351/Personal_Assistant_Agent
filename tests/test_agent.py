"""
Integration tests for the full agent loop.
Run: pytest tests/test_agent.py -v -s
"""
import pytest
from src.agent.agent_loop import run_agent


def test_agent_weather_query():
    result = run_agent("What's the weather in Mumbai?")
    assert result["answer"]
    assert any(tc["tool"] == "get_weather" for tc in result["tool_calls_made"])
    print(f"\n✅ Weather query: {result['answer']}")


def test_agent_calculator_query():
    result = run_agent("Calculate 125 * 8")
    assert "1000" in result["answer"]
    print(f"\n✅ Calc query: {result['answer']}")


def test_agent_multi_tool():
    result = run_agent("Mumbai weather and what is 50 * 4?")
    assert len(result["tool_calls_made"]) >= 2
    print(f"\n✅ Multi-tool: {result['answer']}")


def test_agent_no_tool_needed():
    result = run_agent("Hello, who are you?")
    assert result["answer"]
    # Greeting ke liye tools needed nahi
    print(f"\n✅ No-tool: {result['answer']}")