import sys
import os
import json

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.mcp_tools import add_task, list_tasks, delete_task
from agents.chatbot_agent import ChatbotAgent
from models.database import User, Task
from core.database import get_session
from datetime import datetime

def test_raw_tools():
    print("\n--- Testing Raw Tools ---")
    user_id = "test_tool_user"
    
    # Ensure user exists
    db_gen = get_session()
    with next(db_gen) as db:
        user = db.get(User, user_id)
        if not user:
            print("Creating test user for tools...")
            new_user = User(id=user_id, email="tool_test@example.com", name="Tool Tester", created_at=datetime.utcnow())
            db.add(new_user)
            db.commit()

    # 1. Add Task
    print("1. Adding Task...")
    task = add_task(user_id, "Raw Tool Task", "Description from raw tool")
    print(f"Task Added: {task['id']} - {task['title']}")
    
    # 2. List Tasks
    print("2. Listing Tasks...")
    tasks = list_tasks(user_id)
    print(f"Tasks found: {len(tasks)}")
    
    # 3. Delete Task
    print("3. Deleting Task...")
    success = delete_task(user_id, task['id'])
    print(f"Delete Success: {success}")

def test_agent_tool_use():
    print("\n--- Testing Agent Tool Use ---")
    agent = ChatbotAgent()
    import uuid
    user_id = f"test_user_{uuid.uuid4().hex[:8]}"
    print(f"Testing with User ID: {user_id}")
    
    # Create user first
    db_gen = get_session()
    with next(db_gen) as db:
        new_user = User(id=user_id, email=f"{user_id}@example.com", name="Agent Tester", created_at=datetime.utcnow())
        db.add(new_user)
        db.commit()

    message = "Search for a task called 'Lunch'"
    print(f"Sending User Message: {message}")
    
    try:
        response = agent.process_message(user_id, message)
        
        print("\nAgent Response Dictionary (Search):")
        print(response.keys())
        
        if response.get("tool_calls"):
            for tc in response['tool_calls']:
                print(f" - Tool: {tc['name']}")
                print(f" - Args: {tc['arguments']}")
                print(f" - Result: {tc['result']}")
        
        print(f"\nFinal Response Text: {response.get('response')}")

    except Exception as e:
        print(f"Agent Search Failed: {e}")

    message = "Add a task called 'Agent Task' with description 'Created via Agent'"
    print(f"\nSending User Message: {message}")
    
    try:
        response = agent.process_message(user_id, message)
        
        print("\nAgent Response Dictionary:")
        # Print keys to avoid huge dump if response is long
        print(response.keys())
        
        if response.get("tool_calls"):
            print(f"Tool Calls made: {len(response['tool_calls'])}")
            for tc in response['tool_calls']:
                print(f" - Tool: {tc['name']}")
                print(f" - Args: {tc['arguments']}")
                print(f" - Result: {tc['result']}")
        else:
            print("NO TOOL CALLS MADE.")
            
        print(f"\nFinal Response Text: {response.get('response')}")
        
    except Exception as e:
        print(f"Agent Execution Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # test_raw_tools()
    test_agent_tool_use()
