from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "Filahaty API"
    VERSION: str = "2.1.0"
    DEBUG: bool = False
    
    # Security
    ALLOWED_ORIGINS: list[str] = [
        "https://filahaty-backend.onrender.com",
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    
    # API Keys (Validated)
    DEEPSEEK_API_KEY: Optional[str] = None
    NEWS_API_KEY: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()
