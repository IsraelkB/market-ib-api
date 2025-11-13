from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional
from utils_folder.get_path import get_path

BASE_DIR = get_path()
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
israel_whatsapp_settings = IsraelWhatsappSettings()
jac_whatsapp_settings = JacWhatsappSettings()
aws_credentials_settings = AWSCredentialsSettings()