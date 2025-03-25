import os
from typing import Optional, List
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Settings(BaseSettings):
    # MongoDB Configuration
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "utdrs")
    
    # Integration URLs
    API_GATEWAY_URL: str = os.getenv("API_GATEWAY_URL", "https://utdrs-api-gateway.onrender.com")
    CORE_ENGINE_URL: str = os.getenv("CORE_ENGINE_URL", "https://utdrs-core-engine.onrender.com")
    RESPONSE_SERVICE_URL: str = os.getenv("RESPONSE_SERVICE_URL", "https://response-service.onrender.com")
    
    # Simulation Settings
    SIMULATION_INTERVAL: int = int(os.getenv("SIMULATION_INTERVAL", "30"))  # seconds
    
    # Fix for the JSON parsing error: use a custom validator
    @property
    def ENABLED_SCENARIOS(self) -> List[str]:
        scenarios_str = os.getenv("ENABLED_SCENARIOS", "phishing,ransomware,data_exfiltration,brute_force,insider_threat")
        return [s.strip() for s in scenarios_str.split(",") if s.strip()]
    
    # App Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    class Config:
        env_file = ".env"

settings = Settings()