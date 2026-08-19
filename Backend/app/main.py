from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.candidate import router as candidate_router
from app.routes.resume import router as resume_router



app = FastAPI(
    title="AI Resume Screening System",
    description="AI-powered resume screening and candidate shortlisting system",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Resume Screening System API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/database-test")
def database_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        result.fetchone()

    return {
        "database": "connected"
    }


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(candidate_router)
app.include_router(resume_router)