from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOSTNAME: str  
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_USERNAME: str
    DATABASE_NAME: str  
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRED_MINUTES: int
    ALGORITHM: str 

    class Config:
        env_file = ".env"
        
settings = Settings()


