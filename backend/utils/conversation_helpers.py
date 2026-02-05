from sqlmodel import Session, select
from models.database import Conversation, Message
from typing import List, Optional


def get_conversation_history(
    db: Session, conversation_id: int, user_id: str
) -> Optional[List[Message]]:
    """
    Retrieve conversation history for a given conversation ID and user ID.
    
    Args:
        db: Database session
        conversation_id: ID of the conversation to retrieve
        user_id: ID of the user requesting the history
        
    Returns:
        List of messages in the conversation, or None if conversation doesn't exist
    """
    # Verify the conversation belongs to the user
    conversation = db.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user_id:
        return None
    
    # Get all messages in the conversation
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = db.exec(statement).all()
    
    return messages


def create_new_conversation(db: Session, user_id: str) -> Conversation:
    """
    Create a new conversation for a user.
    
    Args:
        db: Database session
        user_id: ID of the user creating the conversation
        
    Returns:
        The newly created conversation
    """
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return conversation


def save_message_to_conversation(
    db: Session, conversation_id: int, user_id: str, role: str, content: str
) -> Message:
    """
    Save a message to a conversation.
    
    Args:
        db: Database session
        conversation_id: ID of the conversation to save to
        user_id: ID of the user sending the message
        role: Role of the sender ('user' or 'assistant')
        content: Content of the message
        
    Returns:
        The saved message
    """
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message