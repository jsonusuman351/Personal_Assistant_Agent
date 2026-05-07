"""
Unit tests for individual tools.

Mock tests  → always run in CI (no API keys needed)
Real tests  → skip automatically if API key is not set

Run all:         pytest tests/test_tools.py -v
Run mock only:   pytest tests/test_tools.py -v -m "not real_api"
Run real only:   pytest tests/test_tools.py -v -m "real_api"
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError, RequestException

from src.tools.weather_tool import get_weather
from src.tools.calculator_tool import calculator
from src.tools.search_tool import web_search


# ── Skip markers for real API tests ────────────────────────────────────────
needs_weather_key = pytest.mark.skipif(
    not os.getenv("OPENWEATHER_API_KEY"),
    reason="OPENWEATHER_API_KEY not set — skipping real API test"
)
needs_tavily_key = pytest.mark.skipif(
    not os.getenv("TAVILY_API_KEY"),
    reason="TAVILY_API_KEY not set — skipping real API test"
)


# ── Helper ──────────────────────────────────────────────────────────────────
def make_mock_response(status_code=200, json_data=None):
    """Build a fake requests.Response for mocking."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data or {}
    if status_code >= 400:
        mock_resp.raise_for_status.side_effect = HTTPError(response=mock_resp)
    else:
        mock_resp.raise_for_status.return_value = None
    return mock_resp


# ═══════════════════════════════════════════════════════════════════════════
# CALCULATOR — pure Python, no API, no mock needed
# ═══════════════════════════════════════════════════════════════════════════

class TestCalculator:

    def test_simple_multiplication(self):
        assert "100" in calculator("25 * 4")

    def test_simple_addition(self):
        assert "15" in calculator("10 + 5")

    def test_simple_subtraction(self):
        assert "-10" in calculator("10 - 20")

    def test_complex_expression(self):
        assert "10.0" in calculator("(10 + 5) * 2 / 3")

    def test_modulo(self):
        assert "1" in calculator("10 % 3")

    def test_power(self):
        assert "256" in calculator("2 ** 8")

    def test_division_by_zero(self):
        result = calculator("10 / 0")
        assert "zero" in result.lower()

    def test_invalid_expression_blocked(self):
        # Security: imports and function calls must be rejected
        assert "Invalid" in calculator("import os")
        assert "Invalid" in calculator("__import__('os')")

    def test_empty_expression(self):
        result = calculator("")
        assert "error" in result.lower() or "invalid" in result.lower() or "Result" not in result

    def test_decimal_result(self):
        assert "3.5" in calculator("7 / 2")

    # Percentage tests
    def test_percentage_of(self):
        assert "100.0" in calculator("20% of 500")

    def test_percentage_add(self):
        assert "600.0" in calculator("500 + 20%")

    def test_percentage_subtract(self):
        assert "425.0" in calculator("500 - 15%")

    def test_percentage_bare(self):
        assert "0.2" in calculator("20%")

    def test_percentage_case_insensitive(self):
        assert "100.0" in calculator("20% OF 500")


def test_percentage_calculation():
    assert "100.0" in calculator("20% of 500")
    assert "600.0" in calculator("500 + 20%")
    assert "425.0" in calculator("500 - 15%")
    assert "0.2"   in calculator("20%")


# ═══════════════════════════════════════════════════════════════════════════
# WEATHER — mocked (CI safe) + real (optional)
# ═══════════════════════════════════════════════════════════════════════════

WEATHER_MOCK_DATA = {
    "main": {"temp": 28.5, "feels_like": 30.0, "humidity": 75},
    "weather": [{"description": "clear sky"}]
}


class TestWeatherMock:
    """Mock tests — no API key needed, always run in CI."""

    @patch("src.tools.weather_tool.requests.get")
    def test_success_returns_formatted_string(self, mock_get):
        mock_get.return_value = make_mock_response(json_data=WEATHER_MOCK_DATA)
        result = get_weather("Mumbai")
        assert "Mumbai" in result
        assert "28.5°C" in result
        assert "clear sky" in result
        assert "75%" in result

    @patch("src.tools.weather_tool.requests.get")
    def test_city_not_found_returns_friendly_message(self, mock_get):
        mock_get.return_value = make_mock_response(status_code=404)
        result = get_weather("InvalidCityXYZ123")
        assert "not found" in result.lower()

    @patch("src.tools.weather_tool.requests.get")
    def test_network_error_handled_gracefully(self, mock_get):
        mock_get.side_effect = RequestException("Network down")
        result = get_weather("Mumbai")
        assert "error" in result.lower() or "network" in result.lower()

    @patch("src.tools.weather_tool.requests.get")
    def test_feels_like_included_in_output(self, mock_get):
        mock_get.return_value = make_mock_response(json_data=WEATHER_MOCK_DATA)
        result = get_weather("Delhi")
        assert "30.0°C" in result  # feels_like value

    @patch("src.tools.weather_tool.requests.get")
    def test_correct_api_endpoint_called(self, mock_get):
        mock_get.return_value = make_mock_response(json_data=WEATHER_MOCK_DATA)
        get_weather("Chennai")
        called_url = mock_get.call_args[0][0]
        assert "openweathermap" in called_url

    @patch("src.tools.weather_tool.requests.get")
    def test_metric_units_used(self, mock_get):
        mock_get.return_value = make_mock_response(json_data=WEATHER_MOCK_DATA)
        get_weather("Pune")
        call_params = mock_get.call_args[1]["params"]
        assert call_params.get("units") == "metric"


class TestWeatherReal:
    """Real API tests — skipped in CI if key not set."""

    @pytest.mark.real_api
    @needs_weather_key
    def test_valid_city(self):
        result = get_weather("Mumbai")
        assert "Mumbai" in result
        assert "°C" in result

    @pytest.mark.real_api
    @needs_weather_key
    def test_invalid_city(self):
        result = get_weather("InvalidCityXYZ123")
        assert "not found" in result.lower() or "error" in result.lower()


# ═══════════════════════════════════════════════════════════════════════════
# WEB SEARCH — mocked (CI safe) + real (optional)
# ═══════════════════════════════════════════════════════════════════════════

SEARCH_MOCK_DATA = {
    "results": [
        {"title": "Python Docs", "content": "Python is a versatile language", "url": "https://python.org"},
        {"title": "Real Python",  "content": "Learn Python with tutorials",  "url": "https://realpython.com"},
        {"title": "PyPI",         "content": "Python package repository",    "url": "https://pypi.org"},
    ]
}


class TestWebSearchMock:
    """Mock tests — no API key needed, always run in CI."""

    @patch("src.tools.search_tool.requests.post")
    def test_success_returns_formatted_results(self, mock_post):
        mock_post.return_value = make_mock_response(json_data=SEARCH_MOCK_DATA)
        result = web_search("Python programming")
        assert "Python" in result
        assert "python.org" in result

    @patch("src.tools.search_tool.requests.post")
    def test_empty_results_returns_no_results_message(self, mock_post):
        mock_post.return_value = make_mock_response(json_data={"results": []})
        result = web_search("xyzabc123unusualquery")
        assert "no results" in result.lower()

    @patch("src.tools.search_tool.requests.post")
    def test_network_error_handled_gracefully(self, mock_post):
        mock_post.side_effect = RequestException("Connection refused")
        result = web_search("Python")
        assert "failed" in result.lower() or "error" in result.lower()

    @patch("src.tools.search_tool.requests.post")
    def test_max_results_respected(self, mock_post):
        mock_post.return_value = make_mock_response(json_data=SEARCH_MOCK_DATA)
        result = web_search("Python", max_results=2)
        assert "1." in result
        assert "2." in result
        assert "3." not in result  # third result should be cut off

    @patch("src.tools.search_tool.requests.post")
    def test_query_included_in_output(self, mock_post):
        mock_post.return_value = make_mock_response(json_data=SEARCH_MOCK_DATA)
        result = web_search("Python programming")
        assert "Python programming" in result

    @patch("src.tools.search_tool.requests.post")
    def test_correct_api_endpoint_called(self, mock_post):
        mock_post.return_value = make_mock_response(json_data=SEARCH_MOCK_DATA)
        web_search("test")
        called_url = mock_post.call_args[0][0]
        assert "tavily" in called_url


class TestWebSearchReal:
    """Real API tests — skipped in CI if key not set."""

    @pytest.mark.real_api
    @needs_tavily_key
    def test_basic_search(self):
        result = web_search("Python programming")
        assert "Python" in result or "results" in result.lower()


# ═══════════════════════════════════════════════════════════════════════════
# HOW TO ADD TESTS FOR A NEW TOOL
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. Add a skip marker if the tool needs an API key:
#       needs_mytool_key = pytest.mark.skipif(
#           not os.getenv("MYTOOL_API_KEY"), reason="..."
#       )
#
# 2. Create a Mock class (always runs in CI):
#       class TestMyToolMock:
#           @patch("src.tools.my_tool.requests.get")
#           def test_success(self, mock_get):
#               mock_get.return_value = make_mock_response(json_data={...})
#               result = my_tool("input")
#               assert "expected" in result
#
# 3. Create a Real class (skipped if no key):
#       class TestMyToolReal:
#           @pytest.mark.real_api
#           @needs_mytool_key
#           def test_live(self):
#               result = my_tool("real input")
#               assert "expected" in result
