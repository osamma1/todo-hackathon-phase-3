import sys
import os
import logging

# Disable logging
logging.basicConfig(level=logging.CRITICAL)
logging.getLogger("sqlalchemy.engine").setLevel(logging.CRITICAL)
logging.getLogger("sqlalchemy.pool").setLevel(logging.CRITICAL)
logging.getLogger("sqlalchemy.dialects").setLevel(logging.CRITICAL)
logging.getLogger("sqlalchemy.orm").setLevel(logging.CRITICAL)

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_session, engine
from agents.chatbot_agent import ChatbotAgent
from models.database import User, Task
from datetime import datetime

# Direct SQL alchemy echo disable in case
engine.echo = False

def test_delete_only():
    print("Initializing ChatbotAgent...")
    try:
        agent = ChatbotAgent()
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return

    user_id = "test_user_del"
    
    # Setup User
    with next(get_session()) as db:
        user = db.get(User, user_id)
        if not user:
            new_user = User(id=user_id, email="del@test.com", name="Del User", created_at=datetime.utcnow())
            db.add(new_user)
            db.commit()
    
    # Create Task directly in DB to delete
    print("Creating task to delete...")
    with next(get_session()) as db:
        t = Task(user_id=user_id, title="Delete Me Task", description="To be deleted", completed=False)
        db.add(t)
        db.commit()
        db.refresh(t)
        print(f"Task created with ID: {t.id}")

    # Send Message
    msg = "Delete the task 'Delete Me Task'"
    print(f"User Message: '{msg}'")
    
    try:
        response = agent.process_message(user_id=user_id, message=msg)
        print("Response received.")
        print(f"AI Response: {response.get('response')}")
        print(f"Tool Calls: {response.get('tool_calls')}")
    except Exception as e:
        print(f"\nCRITICAL FAIL Caught in Test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_delete_only()
