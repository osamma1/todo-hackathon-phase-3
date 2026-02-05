from sqlmodel import Session, select
from models.database import Task, User
from typing import Optional, Any
from datetime import datetime


def add_task(user_id: str, title: str, description: Optional[str] = None) -> dict:
    """
    Add a new task for the user.
    
    Args:
        user_id: ID of the user adding the task
        title: Title of the task
        description: Optional description of the task
        
    Returns:
        Dictionary with the created task details
    """
    from core.database import get_session  # Import here to avoid circular imports
    
    with next(get_session()) as db:
        # Create new task
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False
        )
        
        db.add(task)
        db.commit()
        db.refresh(task)
        
        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }


def list_tasks(user_id: str, status: Optional[str] = None) -> list:
    """
    List tasks for the user with optional status filter.
    
    Args:
        user_id: ID of the user whose tasks to list
        status: Optional status filter ("all", "pending", "completed")
        
    Returns:
        List of tasks matching the criteria
    """
    from core.database import get_session  # Import here to avoid circular imports
    
    with next(get_session()) as db:
        # Build query with user isolation
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter if provided
        if status and status != "all":
            if status == "completed":
                query = query.where(Task.completed == True)
            elif status == "pending":
                query = query.where(Task.completed == False)

        tasks = db.exec(query).all()
        
        # Convert tasks to dictionaries
        tasks_list = []
        for task in tasks:
            tasks_list.append({
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            })
        
        return tasks_list


def update_task(
    user_id: str, task_id: Any, title: Optional[str] = None, 
    description: Optional[str] = None
) -> dict:
    """
    Update an existing task for the user.
    
    Args:
        user_id: ID of the user whose task to update
        task_id: ID of the task to update (can be int or string)
        title: Optional new title
        description: Optional new description
        
    Returns:
        Updated task details or error message
    """
    from core.database import get_session
    
    try:
        task_id_int = int(task_id)
    except (ValueError, TypeError):
        return {"error": f"Invalid task ID format: {task_id}. ID must be a number."}
    
    with next(get_session()) as db:
        # Get the task
        task = db.get(Task, task_id_int)

        if not task:
            return {"error": "Task not found"}

        # Verify user owns the task
        if task.user_id != user_id:
            return {"error": "Access denied: Task does not belong to user"}

        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        task.updated_at = datetime.utcnow()

        db.add(task)
        db.commit()
        db.refresh(task)

        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }


def complete_task(user_id: str, task_id: Any) -> dict:
    """
    Mark a task as completed for the user.
    
    Args:
        user_id: ID of the user whose task to complete
        task_id: ID of the task to complete
        
    Returns:
        Updated task details or error message
    """
    from core.database import get_session
    
    try:
        task_id_int = int(task_id)
    except (ValueError, TypeError):
        return {"error": f"Invalid task ID format: {task_id}. ID must be a number."}
    
    with next(get_session()) as db:
        # Get the task
        task = db.get(Task, task_id_int)

        if not task:
            return {"error": "Task not found"}

        # Verify user owns the task
        if task.user_id != user_id:
            return {"error": "Access denied: Task does not belong to user"}

        # Update completion status
        task.completed = True
        task.updated_at = datetime.utcnow()

        db.add(task)
        db.commit()
        db.refresh(task)

        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }


def delete_task(user_id: str, task_id: Any) -> dict:
    """
    Delete a task for the user.

    Args:
        user_id: ID of the user whose task to delete
        task_id: ID of the task to delete

    Returns:
        True if successful, False if task not found
    """
    from core.database import get_session
    
    try:
        task_id_int = int(task_id)
    except (ValueError, TypeError):
        return {"success": False, "error": f"Invalid task ID format: {task_id}. ID must be a number."}

    with next(get_session()) as db:
        # Get the task
        task = db.get(Task, task_id_int)

        if not task:
            return {"success": False, "error": "Task not found"}

        # Verify user owns the task
        if task.user_id != user_id:
            return {"success": False, "error": "Access denied: Task does not belong to user"}

        db.delete(task)
        db.commit()

        return {"success": True, "message": "Task deleted successfully"}


def get_user_info(user_id: str) -> Optional[dict]:
    """
    Get user information.

    Args:
        user_id: ID of the user to retrieve information for

    Returns:
        User information if found, None otherwise
    """
    from core.database import get_session  # Import here to avoid circular imports

    with next(get_session()) as db:
        # Get the user
        user = db.get(User, user_id)

        if not user:
            return {"error": "User not found"}

        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at.isoformat()
        }


def search_tasks(user_id: str, query: str) -> list:
    """
    Search tasks for the user by title.
    
    Args:
        user_id: ID of the user whose tasks to search
        query: Search query string
        
    Returns:
        List of tasks matching the query
    """
    from core.database import get_session
    
    with next(get_session()) as db:
        # Build query with case-insensitive title search
        from sqlalchemy import func
        db_query = select(Task).where(
            Task.user_id == user_id,
            func.lower(Task.title).contains(query.lower())
        )
        
        tasks = db.exec(db_query).all()
        
        tasks_list = []
        for task in tasks:
            tasks_list.append({
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            })
            
        return tasks_list