from sqlmodel import Session, SQLModel, select
from core.database import engine
from models.database import User, Task
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        # Create tables if they don't exist
        SQLModel.metadata.create_all(engine)
        
        # Try to connect and select 1
        with Session(engine) as session:
            session.exec(select(1)).first()
            print("Successfully connected to Neon Database!")
            
            # Check if tables exist
            user_count = session.exec(select(User)).first()
            print(f"Database tables are accessible. User check: {user_count is not None}")
            
    except Exception as e:
        print(f"Failed to connect to Neon Database: {e}")

if __name__ == "__main__":
    test_connection()
