from datetime import datetime, timedelta
from typing import Optional
import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlmodel import Session, select
from models.database import User
from core.database import get_session

# Load environment variables
load_dotenv()

# Get the secret key from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"


def verify_token(token: str) -> Optional[dict]:
    """
    Verify the JWT token and return the payload if valid
    """
    try:
        if not SECRET_KEY:
            print("❌ Error: BETTER_AUTH_SECRET is not set in environment!")
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            print(f"❌ Error: token has no user_id. Payload: {payload}")
            return None
        return payload
    except jwt.exceptions.ExpiredSignatureError:
        print("❌ Error: Token has expired")
        return None
    except jwt.exceptions.InvalidTokenError as e:
        print(f"❌ Error: Invalid token: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: Token verification failed: {e}")
        return None


def get_current_user(token: str) -> Optional[User]:
    """
    Get the current user from the token
    """
    # Remove 'Bearer ' prefix if present
    if token.startswith("Bearer "):
        token = token[7:]
    
    payload = verify_token(token)
    if payload is None:
        print(f"❌ Auth Failed: verify_token returned None for token starting with {token[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - verification failed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Query the user from the database
    from sqlmodel import Session as SQLSession
    from core.database import engine
    with SQLSession(engine) as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        
        # If user doesn't exist in our DB, create them (first API call)
        if user is None:
            # Extract user info from token
            email = payload.get("email", "")
            name = payload.get("name", "")
            
            # Create new user
            user = User(id=user_id, email=email, name=name)
            session.add(user)
            session.commit()
            session.refresh(user)
            # Detach from session to use outside
            # (In SQLModel/SQLAlchemy, you might need to refresh or expunge)
            session.expunge(user)
        else:
            # Detach from session to avoid issues when session closes
            session.expunge(user)
    
    return user