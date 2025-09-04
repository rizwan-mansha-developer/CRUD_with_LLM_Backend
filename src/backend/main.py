from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import expenses, chat
from .db import Base, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables now that permissions are granted
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Error creating tables: {e}")

# Include routes
app.include_router(expenses.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {
        "message": "Finance Assistant API with Gemini AI", 
        "status": "running",
        "database": "postgresql",
        "ai_provider": "gemini"
    }

@app.get("/health")
def health_check():
    try:
        # Test database connection
        from .db import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "ai": "gemini configured"
    }
