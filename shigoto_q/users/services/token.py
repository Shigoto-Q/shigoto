import jwt
from django.conf import settings


def check_user_token(payload_token):
    payload = jwt.decode(
        jwt=payload_token,
        key=settings.SECRET_KEY,
        algorithms=["HS256"],
    )
    return payload.get("user_id")
