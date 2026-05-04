"""
Unit tests for individual tools.
Run: pytest tests/test_tools.py -v
"""
import os
import sys


import pytest
from src.tools.weather_tool import get_weather
from src.tools.calculator_tool import calculator
from src.tools.search_tool import web_search


# ===== WEATHER TESTS =====
def test_weather_valid_city():
    result = get_weather("Mumbai")
    assert "Mumbai" in result
    assert "°C" in result
    print(f"\n✅ Weather test: {result}")


def test_weather_invalid_city():
    result = get_weather("InvalidCityXYZ123")
    assert "not found" in result.lower() or "error" in result.lower()
    print(f"\n✅ Invalid city test: {result}")


# ===== CALCULATOR TESTS =====
def test_calculator_simple():
    result = calculator("25 * 4")
    assert "100" in result
    print(f"\n✅ Calc test: {result}")


def test_calculator_complex():
    result = calculator("(10 + 5) * 2 / 3")
    assert "10.0" in result
    print(f"\n✅ Complex calc: {result}")


def test_calculator_division_by_zero():
    result = calculator("10 / 0")
    assert "zero" in result.lower()
    print(f"\n✅ Div by zero: {result}")


def test_calculator_invalid():
    result = calculator("import os")
    assert "Invalid" in result
    print(f"\n✅ Security test: {result}")


# ===== SEARCH TESTS =====
def test_search_basic():
    result = web_search("Python programming")
    assert "Python" in result or "results" in result.lower()
    print(f"\n✅ Search test: {result[:200]}...")