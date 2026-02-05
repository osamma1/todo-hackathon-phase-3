from sqlmodel import select
from core.database import get_session, engine
from models.database import Task, Message, Conversation
import logging

# Disable logs for this script
logging.basicConfig(level=logging.CRITICAL)

def verify_state():
    print("Verifying Database State for 'test_user_crud'...")
    with next(get_session()) as db:
        # Check Tasks
        tasks = db.exec(select(Task).where(Task.user_id == "test_user_crud")).all()
        print(f"\nRemaining Tasks: {len(tasks)}")
        for t in tasks:
            print(f" - {t.title} [Completed: {t.completed}] (ID: {t.id})")

        # Check Conversation/Messages
        # Get conversation for this user
        convs = db.exec(select(Conversation).where(Conversation.user_id == "test_user_crud")).all()
        print(f"\nConversations: {len(convs)}")
        
        for conv in convs:
            print(f"\nConversation ID: {conv.id}")
            messages = db.exec(select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at)).all()
            for msg in messages:
                content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                print(f"[{msg.role.upper()}]: {content_preview}")

if __name__ == "__main__":
    verify_state()
