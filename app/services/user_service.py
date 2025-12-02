from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        safe_password = password[:72]
        return pwd_context.hash(safe_password)
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> UserResponse:
        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise ValueError("Email already registered")
        
        hashed_pwd = UserService.hash_password(user_data.password)

        new_user = User(
            name = user_data.name,
            email = user_data.email,
            password = hashed_pwd,
            role = user_data.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return UserResponse.from_orm(new_user)