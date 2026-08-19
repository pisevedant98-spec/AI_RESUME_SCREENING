from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
def upload_resume(
    user_id: int,
    file: UploadFile = File(...)
):

    # Check file type
    allowed_extensions = [".pdf", ".docx"]

    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed"
        )

    # Create unique filename
    filename = f"user_{user_id}_{file.filename}"

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Resume uploaded successfully",
        "user_id": user_id,
        "filename": filename,
        "file_path": file_path
    }


from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

from app.service.resume_service import extract_text_from_pdf


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
def upload_resume(
    user_id: int,
    file: UploadFile = File(...)
):
    allowed_extensions = [".pdf", ".docx"]

    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed"
        )

    filename = f"user_{user_id}_{file.filename}"

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Resume uploaded successfully",
        "user_id": user_id,
        "filename": filename,
        "file_path": file_path
    }


@router.get("/extract/{user_id}")
def extract_resume_text(user_id: int):

    # Find uploaded PDF
    matching_file = None

    for filename in os.listdir(UPLOAD_DIR):
        if filename.startswith(f"user_{user_id}_") and filename.lower().endswith(".pdf"):
            matching_file = os.path.join(UPLOAD_DIR, filename)
            break

    if not matching_file:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    try:
        text = extract_text_from_pdf(matching_file)

        return {
            "user_id": user_id,
            "filename": os.path.basename(matching_file),
            "text": text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not extract resume text: {str(e)}"
        )


from app.service.resume_service import (
    extract_text_from_pdf,
    extract_candidate_details
)           

@router.get("/details/{user_id}")
def get_candidate_details(user_id: int):

    file_path = None

    for filename in os.listdir(UPLOAD_DIR):

        if filename.startswith(f"user_{user_id}_"):
            file_path = os.path.join(
                UPLOAD_DIR,
                filename
            )
            break

    if not file_path:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    text = extract_text_from_pdf(file_path)

    details = extract_candidate_details(text)

    return {
        "user_id": user_id,
        "details": details
    }