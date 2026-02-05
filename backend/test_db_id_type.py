import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sqlmodel import Session, select
from core.database import engine
from models.database import Task

def test_id_type_db():
    with Session(engine) as session:
        # Get any task ID
        task = session.exec(select(Task)).first()
        if not task:
            print("No tasks found to test with.")
            return
        
        task_id_int = task.id
        task_id_str = str(task_id_int)
        
        print(f"Testing with Task ID: {task_id_int} (int) and {task_id_str} (str)")
        
        try:
            results = session.get(Task, task_id_str)
            print(f"session.get with string worked: {results.id if results else 'Not found'}")
        except Exception as e:
            print(f"session.get with string FAILED: {e}")

if __name__ == "__main__":
    test_id_type_db()
