import sys
import os
import asyncio

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_session
from agents.chatbot_agent import ChatbotAgent
from models.database import User
from datetime import datetime
import uuid

def test_chatbot():
    print("Initializing ChatbotAgent...")
    try:
        agent = ChatbotAgent()
        print("ChatbotAgent initialized.")
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return

    user_id = "test_user_chatbot"
    
    # Needs a DB session to create conversation
    db_gen = get_session()
    db = next(db_gen)
    
    # Ensure user exists for FK
    try:
        user = db.get(User, user_id)
        if not user:
            print("Creating test user...")
            new_user = User(
                id=user_id,
                email="test_chatbot_v2@example.com",
                name="Chatbot Test User V2",
                created_at=datetime.utcnow()
            )
            db.add(new_user)
            db.commit()
            print("Test user created.")
    except Exception as e:
        print(f"DB Error creating user: {e}")
        return

    print("Processing message...")
    try:
        response = agent.process_message(
            user_id=user_id,
            message="Hello, can you help me?"
        )
        print("\nResponse received:")
        if 'error' in str(response.get('response', '')).lower():
            print(f"Chatbot returned an error message: {response}")
        else:
            print("Success! Response key present.")
            # print(response) # Optional, don't spam logs
    except Exception as e:
        print(f"\nError processing message: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chatbot()
