from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db


router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"]
)


class CandidateProfile(BaseModel):
    user_id: int
    phone: str
    education: str
    experience: str


@router.post("/profile")
def create_candidate_profile(
    data: CandidateProfile,
    db: Session = Depends(get_db)
):

    # Check whether user exists and is a candidate
    user_query = text("""
        SELECT id, role
        FROM users
        WHERE id = :user_id
    """)

    user = db.execute(
        user_query,
        {"user_id": data.user_id}
    ).fetchone()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role != "candidate":
        raise HTTPException(
            status_code=403,
            detail="Only candidates can create a candidate profile"
        )

    # Check whether profile already exists
    check_query = text("""
        SELECT id
        FROM candidates
        WHERE user_id = :user_id
    """)

    existing = db.execute(
        check_query,
        {"user_id": data.user_id}
    ).fetchone()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Candidate profile already exists"
        )

    # Create candidate profile
    insert_query = text("""
        INSERT INTO candidates
        (user_id, phone, education, experience)
        VALUES
        (:user_id, :phone, :education, :experience)
    """)

    db.execute(
        insert_query,
        {
            "user_id": data.user_id,
            "phone": data.phone,
            "education": data.education,
            "experience": data.experience
        }
    )

    db.commit()

    return {
        "message": "Candidate profile created successfully",
        "user_id": data.user_id
    }