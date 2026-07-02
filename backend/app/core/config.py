from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    database_url: str
    anthropic_api_key: str
    fmp_api_key: str
    supabase_url: str
    supabase_key: str
    class Config:
        env_file = Path(__file__).resolve().parents[3]/ ".env"

settings = Settings ()