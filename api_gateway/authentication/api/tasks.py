import uuid

from api_gateway import settings
from api_gateway.authentication.api.security import create_email_verification_token

def send_email_verification_link(email: str, user_id: uuid.UUID):

    token = create_email_verification_token(user_id)

    verification_link = (
        f"{settings.settings.FRONTEND_URL}/"
    )