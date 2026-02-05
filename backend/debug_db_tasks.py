import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sqlmodel import Session, select
from core.database import engine
from models.database import Task, User
import logging

# Kill all logging
logging.disable(logging.CRITICAL)

def list_all_data():
    output = []
    with Session(engine) as session:
        output.append("--- USERS ---")
        users = session.exec(select(User)).all()
        for u in users:
            output.append(f"ID: {u.id}, Name: {u.name}, Email: {u.email}")
            
        output.append("\n--- TASKS ---")
        tasks = session.exec(select(Task)).all()
        for t in tasks:
            output.append(f"ID: {t.id}, Title: {t.title}, UserID: {t.user_id}, Completed: {t.completed}")
            
    with open("db_snap.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    list_all_data()
