from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlmodel import Session, select
from models.database import Task, User
from schemas.task import TaskRead, TaskCreate, TaskUpdate
from dependencies import get_current_active_user, get_db
from core.security import verify_token
from datetime import datetime

router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    status: Optional[str] = None,
    sort: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all tasks for the authenticated user
    """
    # Build query with user isolation
    query = select(Task).where(Task.user_id == current_user.id)

    # Apply status filter if provided
    if status and status != "all":
        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)

    # Apply sorting if provided
    if sort == "title":
        query = query.order_by(Task.title)
    elif sort == "created":
        query = query.order_by(Task.created_at.desc())  # Most recent first
    elif sort == "due_date":  # Assuming due_date is part of updated_at for now
        query = query.order_by(Task.updated_at.desc())

    tasks = db.exec(query).all()
    return tasks


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user
    """
    # Validate task title length
    if len(task.title) < 1 or len(task.title) > 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title must be between 1 and 200 characters"
        )
    
    # Validate description length if provided
    if task.description and len(task.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task description must be less than 1000 characters"
        )
    
    # Create task with user_id from current user
    db_task = Task(
        title=task.title,
        description=task.description,
        user_id=current_user.id
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific task for the authenticated user
    """
    task = db.get(Task, task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify user owns the task
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a specific task for the authenticated user
    """
    db_task = db.get(Task, task_id)
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify user owns the task
    if db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Update fields if provided
    if task_update.title is not None:
        # Validate title length
        if len(task_update.title) < 1 or len(task_update.title) > 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task title must be between 1 and 200 characters"
            )
        db_task.title = task_update.title
    
    if task_update.description is not None:
        # Validate description length
        if len(task_update.description) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task description must be less than 1000 characters"
            )
        db_task.description = task_update.description
    
    if task_update.completed is not None:
        db_task.completed = task_update.completed
    
    db_task.updated_at = datetime.utcnow()
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific task for the authenticated user
    """
    db_task = db.get(Task, task_id)
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify user owns the task
    if db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    db.delete(db_task)
    db.commit()
    
    return


@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Toggle the completion status of a task
    """
    db_task = db.get(Task, task_id)
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify user owns the task
    if db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Toggle completion status
    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.utcnow()
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task