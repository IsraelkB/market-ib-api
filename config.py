from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

class IBKRSettings(BaseSettings):
    demo_port: int
    port: int
    host: str
    client_id: Optional[int] = None

    model_config = ConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )

class GoogleSettings(BaseSettings):
    smtp_user: str
    smtp_password: str
    recipient_one: str
    recipient_two: str
    model_config = ConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra = "ignore"
    )

class IsraelWhatsappSettings(BaseSettings):
    phone_number_israel: str
    bot_key_israel: str
    base_url_bot: str
    model_config = ConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )

class JacWhatsappSettings(BaseSettings):
    phone_number_israel: str
    bot_key_israel: str
    base_url_bot: str
    model_config = ConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = IBKRSettings()
google_settings = GoogleSettings()
israel_whatsapp_settings = IsraelWhatsappSettings()
jac_whatsapp_settings = JacWhatsappSettings()