from config import aws_credentials_settings
import boto3

def create_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=aws_credentials_settings.aws_access_key_id,
        aws_secret_access_key=aws_credentials_settings.aws_secret_access_key,
        region_name=aws_credentials_settings.region
    )