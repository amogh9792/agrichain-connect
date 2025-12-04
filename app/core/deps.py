from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.logging_config import logger
from app.core.security import JWT_SECRET_KEY, ALGORITHM
from app.database.connection import get_db
from app.models.user import User

# OAuth2 scheme that reads the Bearer token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    logger.info("JWT validation started")

    # Step 1: Decode JWT token
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            logger.warning("JWT validation failed: 'sub' claim missing in token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"JWT decoded successfully for email={email}")

    except JWTError as e:
        logger.warning(f"JWT decode error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 2: Fetch user from database
    user = db.query(User).filter(User.email == email).first()

    if not user:
        logger.warning(f"JWT validation failed: user not found in DB for email={email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logger.info(f"JWT validation successful. User resolved: id={user.id}, email={user.email}")
    return user
