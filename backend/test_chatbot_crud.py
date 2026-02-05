import sys
import os
import logging

# Disable logging
logging.basicConfig(level=logging.CRITICAL)
logging.getLogger("sqlalchemy.engine").setLevel(logging.CRITICAL)
logging.getLogger("sqlalchemy.pool").setLevel(logging.CRITICAL)
logging.getLogger("sqlalchemy.dialects").setLevel(logging.CRITICAL)
logging.getLogger("sqlalchemy.orm").setLevel(logging.CRITICAL)

import time

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_session
from agents.chatbot_agent import ChatbotAgent
from models.database import User, Task
from datetime import datetime
from sqlmodel import select


def print_separator(title):
    print("\n" + "="*50)
    print(f" {title} ")
    print("="*50)

def test_chatbot_crud():
    print("Initializing ChatbotAgent for CRUD Test...")
    try:
        agent = ChatbotAgent()
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return

    user_id = "test_user_crud"
    
    # 1. Setup User
    print_separator("1. Setting up Test User")
    db_gen = get_session()
    db = next(db_gen)
    
    try:
        user = db.get(User, user_id)
        if not user:
            print(f"Creating test user {user_id}...")
            new_user = User(
                id=user_id,
                email="test_crud@example.com",
                name="Chatbot CRUD Tester",
                created_at=datetime.utcnow()
            )
            db.add(new_user)
            db.commit()
            print("Test user created.")
        else:
            print("Test user already exists.")
            
        # Clean up existing tasks for this user to start fresh
        existing_tasks = db.exec(select(Task).where(Task.user_id == user_id)).all()
        for t in existing_tasks:
            db.delete(t)
        db.commit()
        print("Cleaned up existing tasks for clean state.")
        
    except Exception as e:
        print(f"DB Setup Error: {e}")
        return

    # Helper to send message
    def send_message(msg, step_name):
        print_separator(f"Testing: {step_name}")
        print(f"User Message: '{msg}'")
        try:
            # We use a new conversation ID for simplicity or let it generate one
            # For this test, we can let it create a new one for the first msg, then reuse? 
            # Actually, `process_message` handles conversation creation if `conversation_id` is None.
            # But the agent creates a NEW conversation if ID is None. 
            # To simulate a flow, we should capture the conversation_id from the first response.
            
            response = agent.process_message(
                user_id=user_id,
                message=msg
            )
            
            print(f"AI Response: {response.get('response')}")
            
            tool_calls = response.get('tool_calls', [])
            if tool_calls:
                print(f"Tool Calls Executed: {len(tool_calls)}")
                for tc in tool_calls:
                    print(f" - Tool: {tc['name']}")
                    print(f" - Args: {tc['arguments']}")
                    print(f" - Result: {tc['result']}")
            else:
                print("No tool calls executed.")
                
            return response.get('conversation_id')
                
        except Exception as e:
            print(f"Error in {step_name}: {e}")
            import traceback
            traceback.print_exc()
            return None

    # 2. Test CREATE
    current_conv_id = send_message("Add a task called 'Test Chatbot CRUD'", "CREATE TASK")
    
    # 3. Test READ
    # Pass the conversation ID to maintain context if needed, but the agent code currently 
    # looks up conversation by ID. If we pass None, it creates a new one.
    # The agent state (history) is saved in DB. 
    # Let's try to maintain conversation ID if possible, but `process_message` signature:
    # def process_message(self, user_id: str, message: str, conversation_id: int = None):
    # So we should pass it back.
    
    send_message("List all my tasks", "READ TASKS")

    # 4. Test UPDATE (Mark as Complete)
    # The prompt should be specific enough to trigger the tool.
    # "Mark 'Test Chatbot CRUD' as complete" might trigger search first, then complete.
    # The system prompt says: "If a user refers to a task by name, you MUST first use search_tasks or list_tasks..."
    send_message("Mark the task 'Test Chatbot CRUD' as complete", "UPDATE TASK (COMPLETE)")

    # 5. Verify in DB
    print_separator("Verifying in Database")
    with next(get_session()) as db:
        tasks = db.exec(select(Task).where(Task.user_id == user_id)).all()
        for t in tasks:
            print(f"Task: {t.title}, ID: {t.id}, Completed: {t.completed}")
            if t.title == 'Test Chatbot CRUD' and t.completed:
                print("SUCCESS: Task found and marked as completed.")
            elif t.title == 'Test Chatbot CRUD' and not t.completed:
                print("FAILURE: Task found but NOT completed.")

    # 6. Test DELETE
    send_message("Delete the task 'Test Chatbot CRUD'", "DELETE TASK")
    
    # 7. Final Verify
    print_separator("Final Verification")
    with next(get_session()) as db:
        tasks = db.exec(select(Task).where(Task.user_id == user_id)).all()
        if not tasks:
            print("SUCCESS: Task deleted.")
        else:
            print(f"FAILURE: Tasks still exist: {len(tasks)}")

if __name__ == "__main__":
    test_chatbot_crud()
