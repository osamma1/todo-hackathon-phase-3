from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from models.database import User
from dependencies import get_current_active_user, get_db
from agents.chatbot_agent import ChatbotAgent
from typing import Optional
from pydantic import BaseModel
import logging
from datetime import datetime, timedelta

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory rate limiting storage (in production, use Redis or similar)
# Key: user_id, Value: list of request timestamps
rate_limit_storage = {}
RATE_LIMIT = 100  # 100 requests per hour
RATE_LIMIT_WINDOW = timedelta(hours=1)


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


def check_rate_limit(user_id: str) -> bool:
    """
    Check if the user has exceeded the rate limit.

    Args:
        user_id: ID of the user making the request

    Returns:
        True if within rate limit, False if exceeded
    """
    now = datetime.utcnow()
    window_start = now - RATE_LIMIT_WINDOW

    # Get user's request history
    user_requests = rate_limit_storage.get(user_id, [])

    # Remove requests outside the current window
    user_requests = [req_time for req_time in user_requests if req_time > window_start]

    # Check if rate limit exceeded
    if len(user_requests) >= RATE_LIMIT:
        return False

    # Add current request to history
    user_requests.append(now)
    rate_limit_storage[user_id] = user_requests

    return True


@router.post("/chat")
async def chat(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Process a chat message and return the AI response.
    """
    # Check rate limit
    if not check_rate_limit(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )

    # Validate input
    if not chat_request.message or len(chat_request.message.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )

    try:
        # Create chatbot agent instance
        agent = ChatbotAgent()

        # Process the message
        result = agent.process_message(
            user_id=current_user.id,
            message=chat_request.message,
            conversation_id=chat_request.conversation_id
        )

        return result
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your message"
        )


# Include the path parameter version for user-specific routes
@router.post("/{user_id}/chat")
async def chat_with_user_id(
    user_id: str,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Process a chat message for a specific user and return the AI response.
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    # Check rate limit
    if not check_rate_limit(user_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )

    # Validate input
    if not chat_request.message or len(chat_request.message.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )

    try:
        # Create chatbot agent instance
        agent = ChatbotAgent()

        # Process the message
        result = agent.process_message(
            user_id=user_id,
            message=chat_request.message,
            conversation_id=chat_request.conversation_id
        )

        return result
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your message"
        )