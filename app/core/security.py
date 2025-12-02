from datetime import datetime, timedelta
from typing import Dict, Any, Optional

import jwt

from app.core.config import settings


def create_access_token(
    data: Dict[str, Any],
    expires_minutes: Optional[int] = None
) -> str:
    """
    Create a JWT access token with expiry.
    `data` usually contains user id or email.
    """
    to_encode = data.copy()

    expire_minutes = expires_minutes or settings.JWT_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)

    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGO
    )
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode a JWT and return its payload.
    Raises jwt exceptions if invalid/expired.
    """
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGO]
    )
    return payload
