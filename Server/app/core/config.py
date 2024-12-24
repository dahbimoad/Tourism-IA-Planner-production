from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"

# Create an instance of the Settings class
settings = Settings()
