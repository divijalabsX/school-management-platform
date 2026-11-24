from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from app.core.config import settings


def create_access_token(user_id: UUID) -> str:
    """
    Generate a signed JWT access token for an authenticated user.
    """

    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def verify_access_token(token: str) -> dict:
    """
    Verify a JWT token and return its decoded payload.
    """

    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM]
    )

    return payload