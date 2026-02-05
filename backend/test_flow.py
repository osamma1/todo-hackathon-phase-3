import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents.chatbot_agent import ChatbotAgent
from models.database import User, Task
from core.database import get_session
import json

def test_full_search_delete_flow():
    agent = ChatbotAgent()
    user_id = "3b27bce6-3516-48a4-b9c8-112beea61d6b" # Annas
    
    # Ensure 'Lunch' exists
    with next(get_session()) as db:
        from sqlmodel import select
        lunch = db.exec(select(Task).where(Task.user_id == user_id, Task.title == "Lunch")).first()
        if not lunch:
            print("Creating Lunch task for testing...")
            db.add(Task(user_id=user_id, title="Lunch", description="Eat lunch"))
            db.commit()

    # Flow 1: Search for Lunch (Turn 1)
    print("\n--- Phase 1: Search for Lunch ---")
    res1 = agent.process_message(user_id, "What is the ID of my Lunch task?")
    print(f"AI: {res1['response']}")
    conv_id = res1['conversation_id']
    
    # Flow 2: Delete request (Turn 2)
    print("\n--- Phase 2: Delete it ---")
    res2 = agent.process_message(user_id, "Delete that lunch task", conversation_id=conv_id)
    print(f"AI: {res2['response']}")
    print(f"Tool Calls: {json.dumps(res2.get('tool_calls'), indent=2)}")

    # Flow 3: Confirm deletion (Turn 3)
    print("\n--- Phase 3: Confirm deletion ---")
    res3 = agent.process_message(user_id, "yess", conversation_id=conv_id)
    print(f"AI: {res3['response']}")
    print(f"Tool Calls: {json.dumps(res3.get('tool_calls'), indent=2)}")

if __name__ == "__main__":
    test_full_search_delete_flow()
