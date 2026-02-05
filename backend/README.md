# Todo Backend API

A secure, multi-user backend for the Todo application built with FastAPI and SQLModel.

## Features

- JWT-based authentication with Better Auth integration
- Task management with CRUD operations
- User isolation (each user sees only their own tasks)
- Filtering and sorting capabilities
- Neon PostgreSQL database integration
- Docker-ready deployment

## Prerequisites

- Python 3.13+
- UV package manager
- Access to Neon PostgreSQL database
- Better Auth configured on frontend

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd backend
```

### 2. Install Dependencies
```bash
uv init
uv add fastapi sqlmodel uvicorn python-dotenv pyjwt python-jose[cryptography]
```

### 3. Environment Configuration
Create a `.env` file in the backend directory

### 4. Run Development Server
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- All API endpoints require a valid JWT token in the Authorization header
- Token is obtained from Better Auth on the frontend
- Format: `Authorization: Bearer <token>`

### Task Management Endpoints
- `GET /api/tasks` - List user's tasks with filtering and sorting
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task
- `PATCH /api/tasks/{task_id}/complete` - Toggle task completion

## Docker Deployment

To run the application using Docker:

```bash
docker-compose up --build
```

## Project Structure
```
backend/
├── main.py              # FastAPI app with CORS configuration
├── .env                 # Environment variables
├── .env.example         # Example environment variables
├── requirements.txt     # Python dependencies
├── models/              # SQLModel models
│   └── database.py      # User and Task models
├── api/                 # API routers
│   └── tasks.py         # Task endpoints
├── core/                # Core functionality
│   ├── config.py        # Configuration and settings
│   ├── security.py      # JWT verification and authentication
│   ├── database.py      # Database connection and session
│   ├── exceptions.py    # Custom exceptions
│   └── logging.py       # Logging configuration
├── schemas/             # Pydantic schemas
│   ├── user.py          # User schemas
│   └── task.py          # Task schemas
├── dependencies.py      # FastAPI dependencies (get_current_user, get_db)
└── utils/               # Utility functions
    └── helpers.py       # Helper functions
```

## Key Technologies
- FastAPI: Modern, fast web framework for building APIs
- SQLModel: SQL databases with Python, combining SQLAlchemy and Pydantic
- Neon PostgreSQL: Serverless PostgreSQL for scalable database storage
- PyJWT: JSON Web Token implementation for authentication
- python-dotenv: Loading environment variables from .env files

## Integration with Frontend
The backend is designed to work seamlessly with the Next.js frontend:
- JWT tokens from Better Auth are verified using the shared secret
- All endpoints return JSON responses that match frontend expectations
- CORS is configured to allow requests from the frontend URL
- User isolation is enforced at the database level
