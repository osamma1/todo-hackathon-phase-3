import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents.chatbot_agent import ChatbotAgent
from models.database import User, Task
from core.database import get_session
from datetime import datetime
import json

def test_delete_update():
    agent = ChatbotAgent()
    user_id = "3b27bce6-3516-48a4-b9c8-112beea61d6b" # Annas
    
    # 1. Create a task to be deleted/updated
    with next(get_session()) as db:
        new_task = Task(user_id=user_id, title="Temp Task", description="To be deleted")
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        task_id = new_task.id
        print(f"Created Temp Task with ID: {task_id}")

    # 2. Try to update it via agent
    message = f"Update task {task_id} to have title 'Updated Temp'"
    print(f"\nSending Message: {message}")
    response = agent.process_message(user_id, message)
    print(f"Agent Response: {response.get('response')}")
    print(f"Tool Calls: {json.dumps(response.get('tool_calls'), indent=2)}")

    # 3. Try to complete it via agent
    message = f"Mark task {task_id} as complete"
    print(f"\nSending Message: {message}")
    response = agent.process_message(user_id, message)
    print(f"Agent Response: {response.get('response')}")
    print(f"Tool Calls: {json.dumps(response.get('tool_calls'), indent=2)}")

    # 4. Try to delete it via agent
    message = f"Delete task {task_id}"
    print(f"\nSending Message: {message}")
    response = agent.process_message(user_id, message)
    print(f"Agent Response: {response.get('response')}")
    print(f"Tool Calls: {json.dumps(response.get('tool_calls'), indent=2)}")

if __name__ == "__main__":
    test_delete_update()
