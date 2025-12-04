from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.core.logging_config import logger
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import create_access_token

# Same hashing scheme as user_service
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def login(db: Session, login_data: LoginRequest) -> TokenResponse:
        # 1. Find user by email
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user:
            logger.warning(f"Login failed: User not found email = {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email or password",
            )

        # 2. Verify password
        if not AuthService.verify_password(login_data.password, user.password):
            
            logger.warning(f"Login Failed: Invalid password for email = {login_data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email or password",
            )

        # 3. Create JWT (we put user id in "sub")
        token = create_access_token({"sub": str(user.id)})
        logger.info(f"Login Successful for user_id = {user.id}")
        
        # 4. Return token response
        return TokenResponse(access_token=token)
