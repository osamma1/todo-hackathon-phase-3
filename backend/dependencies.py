from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from sqlmodel import Session
from core.database import get_session
import core.security as security
from models.database import User

security_scheme = HTTPBearer(auto_error=False)


def get_db():
    """
    Get database session dependency
    """
    yield next(get_session())


def get_current_user(auth: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)):
    """
    Get current user from token dependency (Mandatory)
    """
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth.credentials
    user = security.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Get current active user dependency (Mandatory)
    """
    return current_user


def get_optional_user(auth: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)) -> Optional[User]:
    """
    Get current user from token dependency (Optional)
    """
    if not auth:
        return None
    try:
        token = auth.credentials
        return security.get_current_user(token)
    except:
        return None