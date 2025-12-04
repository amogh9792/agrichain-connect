from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agrichain Connect"

    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # JWT
    JWT_SECRET: str
    JWT_ALGO: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
