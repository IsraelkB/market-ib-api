from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    demo_port: int
    port: int
    host: str
    client_id: Optional[int] = None

    class Config:
        env_file = "ib_insync_local/.env"

settings = Settings()
