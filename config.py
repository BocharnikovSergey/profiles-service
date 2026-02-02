from pydantic_settings import BaseSettings, SettingsConfigDict
import os
class Settings(BaseSettings):
    APP_NAME: str = "fastapi-service"
    DEBUG: bool = False
    
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", os.getenv("POSTGRES_DB", "mydb"))
    db_user: str = os.getenv("DB_USER", os.getenv("POSTGRES_USER", "postgres"))
    db_pass: str = os.getenv("DB_PASS", os.getenv("POSTGRES_PASSWORD", "1234"))
    test_db_name: str = os.getenv("TEST_DB_NAME",os.getenv("TEST_POSTGRES","user_test_db"))

    db_driver: str = "postgresql+asyncpg"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.test_db_name}"

settings = Settings()