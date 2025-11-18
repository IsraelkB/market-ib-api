from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional
from utils_folder.get_path import get_base_path

BASE_DIR = get_base_path()
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

class WhatsappSettings(BaseSettings):
    bot_url: str
    model_config = ConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )

class AWSCredentialsSettings(BaseSettings):
    bucket_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    region: str
    model_config = ConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = IBKRSettings()
google_settings = GoogleSettings()
whatsapp_settings = WhatsappSettings()
aws_credentials_settings = AWSCredentialsSettings()