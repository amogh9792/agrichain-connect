from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME:str = "Agrichain Connect"

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()