from sqlmodel import create_engine
from typing import Generator
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine if URL is available
if DATABASE_URL:
    engine = create_engine(DATABASE_URL, echo=False)
else:
    print("⚠️ WARNING: DATABASE_URL is not set!")
    engine = None


def get_session() -> Generator:
    from sqlmodel import Session
    with Session(engine) as session:
        yield session