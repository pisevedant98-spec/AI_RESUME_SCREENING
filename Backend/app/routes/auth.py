from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class LoginRequest(BaseModel):
    email: str
    password: str
    role: str


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    # Normalize role
    selected_role = data.role.strip().lower()

    # Check role
    if selected_role not in ["candidate", "hr"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid role. Use 'candidate' or 'hr'."
        )

    # Find user
    query = text("""
        SELECT id, name, email, password, role
        FROM users
        WHERE email = :email
    """)

    result = db.execute(
        query,
        {"email": data.email.strip()}
    ).fetchone()

    # User not found
    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check selected role
    if result.role != selected_role:
        raise HTTPException(
            status_code=403,
            detail="Selected role does not match this account"
        )

    # Check password
    try:
        password_valid = pwd_context.verify(
            data.password,
            result.password
        )
    except Exception:
        password_valid = False

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Login successful
    return {
        "message": "Login successful",
        "user": {
            "id": result.id,
            "name": result.name,
            "email": result.email,
            "role": result.role
        }
    }