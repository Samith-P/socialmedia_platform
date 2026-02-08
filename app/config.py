from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    algorithm: str
    secret_key: str
    access_token_expiration_mins: int

    class Config:
        env_file = "./.env"

settings = Settings()
