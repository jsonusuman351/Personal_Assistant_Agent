"""
Weather Tool - OpenWeather API se current weather fetch karta hai.
"""
import requests
from src.config.settings import settings


def get_weather(city: str) -> str:
    """
    Get current weather for a given city.
    
    Args:
        city: Name of the city (e.g., "Mumbai", "London")
    
    Returns:
        Formatted string with temperature and weather description.
    """
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric"  # Celsius me
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # 4xx/5xx error throw kare
        
        data = response.json()
        
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        feels_like = data["main"]["feels_like"]
        
        return (
            f"Weather in {city}: {temp}°C (feels like {feels_like}°C), "
            f"{description}, humidity: {humidity}%"
        )
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return f"City '{city}' not found. Please check the spelling."
        return f"Weather API error: {e}"
    
    except requests.exceptions.RequestException as e:
        return f"Network error while fetching weather: {e}"
    
    except KeyError as e:
        return f"Unexpected API response format: {e}"