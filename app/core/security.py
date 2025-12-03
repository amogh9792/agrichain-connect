from datetime import datetime, timedelta
from typing import Dict, Any, Optional

import jwt
from app.core.config import settings

# ------------------------------
# Exposed constants (for deps.py)
# ------------------------------
JWT_SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGO
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.JWT_EXPIRE_MINUTES)


def create_access_token(
    data: Dict[str, Any],
    expires_minutes: Optional[int] = None
) -> str:
    """
    Create a JWT access token with expiry.
    """
    to_encode = data.copy()

    expire_minutes = expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)

    to_encode["exp"] = expire

    token = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode JWT and return payload.
    """
    payload = jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[ALGORITHM]
    )
    return payload
