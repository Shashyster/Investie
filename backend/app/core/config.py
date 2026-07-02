from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    database_url: str
    anthropic_api_key: str
    fmp_api_key: str
    supabase_url: str
    supabase_key: str
    class Config:
        env_file = ".env"

settings = Settings ()