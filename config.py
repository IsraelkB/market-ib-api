from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    demo_port: int
    port: int
    host: str
    client_id: Optional[int] = None

    model_config = ConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8"
    )

settings = Settings()
