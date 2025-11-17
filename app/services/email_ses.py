import boto3
from app.core.config import get_settings

settings = get_settings()

ses = boto3.client("ses", region_name=settings.AWS_SES_REGION)

def send_2fa_email(to_email: str, code: str):
    print(f"[DEV] 2FA code: {code}")
