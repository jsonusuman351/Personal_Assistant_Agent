"""
Centralized configuration management.
All environment variables loaded here once.
"""
import os
from dotenv import load_dotenv

# .env file load karo
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    
    # App Config
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "5"))
    
    # Model Config
    MODEL_NAME: str = "gpt-4o-mini"  # cheaper than gpt-4
    TEMPERATURE: float = 0.7
    
    def validate(self):
        """Check ki saari required keys hain ya nahi."""
        required = {
            "OPENAI_API_KEY": self.OPENAI_API_KEY,
            "OPENWEATHER_API_KEY": self.OPENWEATHER_API_KEY,
            "TAVILY_API_KEY": self.TAVILY_API_KEY,
        }
        missing = [k for k, v in required.items() if not v]
        if missing:
            raise ValueError(f"Missing API keys: {missing}")
        return True


# Singleton instance - poore project me yahi use hoga
settings = Settings()