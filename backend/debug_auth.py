import sys
import os
import traceback

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Importing auth...")
    from api.auth import get_password_hash, create_access_token
    from models.database import User
    from core.database import get_session
    from datetime import datetime
    import uuid
    print("Imports successful.")

    print("Testing password hashing...")
    pwd = "password123"
    hashed = get_password_hash(pwd)
    print(f"Hash successful: {hashed[:10]}...")

    print("Testing DB connection...")
    db_gen = get_session()
    db = next(db_gen)
    print("DB Session obtained.")

    print("Attempting to create user...")
    user_id = str(uuid.uuid4())
    # Create a dummy user that won't conflict
    email = f"debug_{user_id[:8]}@example.com"
    
    new_user = User(
        id=user_id, 
        email=email, 
        name="Debug User",
        hashed_password=hashed,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    # We won't commit to avoid cluttering DB, just flush/add
    # db.commit() 
    print("User added to session (not committed).")
    
    print("Debug sequence complete.")

except Exception as e:
    print("\nXXX EXCEPTION CAUGHT XXX")
    traceback.print_exc()
