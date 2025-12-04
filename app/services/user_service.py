from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException
from app.core.logging_config import logger
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    @staticmethod
    def hash_password(password: str) -> str:
        safe_password = password[:72]
        logger.debug("Hashing user password (trimmed to 72 chars)")
        return pwd_context.hash(safe_password)
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> UserResponse:
        logger.info(f"User registration attempt: email={user_data.email}")

        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            logger.warning(f"User registration failed: duplicate email={user_data.email}")
            raise HTTPException(
                status_code=400, 
                detail="Email already registered"
            )
        
        hashed_pwd = UserService.hash_password(user_data.password)
        logger.debug(f"Password hashed for email={user_data.email}")

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_pwd,
            role=user_data.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"User registered successfully: user_id={new_user.id}, email={new_user.email}")

        return UserResponse.from_orm(new_user)
