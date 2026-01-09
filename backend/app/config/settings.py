"""
Configuration settings for the wine inventory management system
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql://wine_user:wine_password@localhost:5432/wine_inventory"
    
    # Application settings
    app_name: str = "Wine Inventory Management System"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # URLs
    backend_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:8080"
    
    # Environment
    environment: str = "DEV" # DEV or PROD
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # External APIs
    vivino_api_key: Optional[str] = None
    stripe_secret_key: Optional[str] = None
    paypal_client_id: Optional[str] = None
    paypal_client_secret: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    hioffice_api_url: Optional[str] = None
    hioffice_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"

    @property
    def is_production(self) -> bool:
        return self.environment.upper() == "PROD"


settings = Settings()

# Override debug mode based on environment
if settings.is_production:
    settings.debug = False
else:
    settings.debug = True