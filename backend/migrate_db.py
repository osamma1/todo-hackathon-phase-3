from sqlmodel import Session, create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def migrate():
    with Session(engine) as session:
        print("Checking users table schema...")
        try:
            # Check if column exists
            session.execute(text("SELECT hashed_password FROM users LIMIT 1"))
            print("Column 'hashed_password' already exists.")
        except Exception:
            print("Adding 'hashed_password' column to 'users' table...")
            session.rollback()
            try:
                session.execute(text("ALTER TABLE users ADD COLUMN hashed_password VARCHAR"))
                session.commit()
                print("Successfully added 'hashed_password' column.")
            except Exception as e:
                print(f"Failed to add column: {e}")

if __name__ == "__main__":
    migrate()
