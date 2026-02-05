import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tools.mcp_tools import add_task, update_task, delete_task, complete_task
from models.database import User, Task
from core.database import get_session
import uuid

def test_type_handling():
    user_id = "test_type_user"
    
    # Ensure user exists
    with next(get_session()) as db:
        user = db.get(User, user_id)
        if not user:
            from datetime import datetime
            new_user = User(id=user_id, email="type_test@example.com", name="Type Tester")
            db.add(new_user)
            db.commit()

    print("1. Adding task...")
    task = add_task(user_id, "Type Test Task")
    task_id_str = task["id"]
    print(f"   Created task ID: {task_id_str} (type: {type(task_id_str)})")

    print("\n2. Trying to update with string ID...")
    try:
        updated = update_task(user_id, task_id_str, title="Updated Title")
        print(f"   Update Result: {updated}")
    except Exception as e:
        print(f"   Update Failed: {e}")

    print("\n3. Trying to complete with string ID...")
    try:
        completed = complete_task(user_id, task_id_str)
        print(f"   Complete Result: {completed}")
    except Exception as e:
        print(f"   Complete Failed: {e}")

    print("\n4. Trying to delete with string ID...")
    try:
        deleted = delete_task(user_id, task_id_str)
        print(f"   Delete Result: {deleted}")
    except Exception as e:
        print(f"   Delete Failed: {e}")

if __name__ == "__main__":
    test_type_handling()
