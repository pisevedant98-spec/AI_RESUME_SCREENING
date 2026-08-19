from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    # Check role
    if data.role not in ["candidate", "hr"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    # Check if email already exists
    check_query = text("""
        SELECT id
        FROM users
        WHERE email = :email
    """)

    existing_user = db.execute(
        check_query,
        {"email": data.email}
    ).fetchone()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = pwd_context.hash(data.password)

    # Insert user
    insert_query = text("""
        INSERT INTO users (name, email, password, role)
        VALUES (:name, :email, :password, :role)
    """)

    db.execute(
        insert_query,
        {
            "name": data.name,
            "email": data.email,
            "password": hashed_password,
            "role": data.role
        }
    )

    db.commit()

    return {
        "message": "Registration successful",
        "user": {
            "name": data.name,
            "email": data.email,
            "role": data.role
        }
    }