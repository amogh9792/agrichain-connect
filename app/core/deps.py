from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.security import ALGORITHM
from app.core.config import settings
from app.models.user import User
from app.database.connection import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)      
) -> User:
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms = [ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401, detail= "User not found.")
        
        return user

    except JWTError: 
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    