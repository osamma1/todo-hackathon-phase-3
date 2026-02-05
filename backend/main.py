from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(title="Todo Backend API", version="1.0.0")

@app.middleware("http")
async def log_requests(request, call_next):
    origin = request.headers.get("origin")
    auth_header = request.headers.get("authorization")
    print(f"📡 Request: {request.method} {request.url.path}")
    print(f"   Origin: {origin}")
    print(f"   Auth: {auth_header[:20] if auth_header else 'None'}...")
    response = await call_next(request)
    print(f"   Response: {response.status_code}")
    return response

# CORS middleware configuration
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    os.getenv("FRONTEND_URL", ""),
    os.getenv("BETTER_AUTH_URL", ""),
]
# Remove empty strings and ensure no trailing slashes
allowed_origins = [origin.rstrip('/') for origin in allowed_origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
    expose_headers=["*"],
)

from api.tasks import router as tasks_router
from api.auth import router as auth_router
from routers.chat import router as chat_router

app.include_router(tasks_router, prefix="/api", tags=["tasks"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(chat_router, prefix="/api", tags=["chat"])

@app.on_event("startup")
async def startup_event():
    # Create database tables
    from sqlmodel import SQLModel
    from core.database import engine
    
    if engine:
        try:
            SQLModel.metadata.create_all(engine)
            print("✅ Database tables verified/created")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
    else:
        print("❌ Skip table creation: engine is None")

@app.get("/")
def read_root():
    return {"message": "Todo Backend API"}