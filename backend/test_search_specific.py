import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents.chatbot_agent import ChatbotAgent
from models.database import User, Task
from core.database import get_session
from datetime import datetime

def test_lunch_search():
    agent = ChatbotAgent()
    user_id = "3b27bce6-3516-48a4-b9c8-112beea61d6b" # User from db_snap who has the Lunch task
    
    # Check if 'Lunch' exists for this user
    with next(get_session()) as db:
        from sqlmodel import select
        lunch_task = db.exec(select(Task).where(Task.user_id == user_id, Task.title == "Lunch")).first()
        if lunch_task:
            print(f"Verified: 'Lunch' task exists for user {user_id}")
        else:
            print(f"Error: 'Lunch' task NOT found for user {user_id}")
            return

    message = "Do I have a task called Lunch?"
    print(f"Sending User Message: {message}")
    
    response = agent.process_message(user_id, message)
    
    print("\nTool Calls:")
    for tc in response.get("tool_calls", []):
        print(f" - Tool: {tc['name']}")
        print(f" - Args: {tc['arguments']}")
        print(f" - Result: {tc['result']}")
        
    print(f"\nFinal Response Text: {response.get('response')}")

if __name__ == "__main__":
    test_lunch_search()
