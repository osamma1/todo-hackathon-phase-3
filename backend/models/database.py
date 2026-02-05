from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from sqlalchemy import CheckConstraint


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True)  # From Better Auth
    email: str = Field(unique=True)
    name: Optional[str] = None
    hashed_password: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)  # Index for efficient filtering by user
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False, index=True)  # Index for efficient filtering by completion status
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: User = Relationship(back_populates="tasks")


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)  # Index for efficient filtering by user
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    __tablename__ = "messages"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant')", name="check_role_valid"),
    )

    id: int = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="users.id")  # Foreign key linking to the user who sent this message
    role: str = Field()  # The role of the sender
    content: str = Field(max_length=5000)  # The actual message content
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")