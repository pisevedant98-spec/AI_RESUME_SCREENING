from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil

from app.service.resume_service import (
    extract_text_from_pdf,
    extract_candidate_details
)


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


# =========================================================
# UPLOAD DIRECTORY
# =========================================================

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================================================
# HELPER: FIND USER RESUME
# =========================================================

def find_user_resume(user_id: int):

    prefix = f"user_{user_id}_"

    if not os.path.exists(UPLOAD_DIR):
        return None

    files = os.listdir(UPLOAD_DIR)

    for filename in files:

        if filename.startswith(prefix):

            extension = os.path.splitext(
                filename
            )[1].lower()

            if extension in [".pdf", ".docx"]:

                return os.path.join(
                    UPLOAD_DIR,
                    filename
                )

    return None


# =========================================================
# UPLOAD RESUME
# =========================================================

@router.post("/upload")
def upload_resume(
    user_id: int,
    file: UploadFile = File(...)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required"
        )

    allowed_extensions = [
        ".pdf",
        ".docx"
    ]

    file_extension = os.path.splitext(
        file.filename
    )[1].lower()

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

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not save resume: {str(e)}"
        )

    return {

        "message": "Resume uploaded successfully",

        "user_id": user_id,

        "filename": filename,

        "file_path": file_path

    }


# =========================================================
# EXTRACT RESUME TEXT
# =========================================================

@router.get("/extract/{user_id}")
def extract_resume_text(user_id: int):

    file_path = find_user_resume(user_id)

    if not file_path:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    extension = os.path.splitext(
        file_path
    )[1].lower()

    # Current extraction function is PDF based.
    if extension != ".pdf":

        raise HTTPException(
            status_code=400,
            detail="Text extraction currently supports PDF resumes"
        )

    try:

        text = extract_text_from_pdf(
            file_path
        )

        return {

            "user_id": user_id,

            "filename": os.path.basename(
                file_path
            ),

            "text": text

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not extract resume text: {str(e)}"
        )


# =========================================================
# GET ONE CANDIDATE DETAILS
# =========================================================

@router.get("/details/{user_id}")
def get_candidate_details(user_id: int):

    file_path = find_user_resume(user_id)

    if not file_path:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension != ".pdf":

        raise HTTPException(
            status_code=400,
            detail="Candidate details currently support PDF resumes"
        )

    try:

        text = extract_text_from_pdf(
            file_path
        )

        details = extract_candidate_details(
            text
        )

        return {

            "user_id": user_id,

            "filename": os.path.basename(
                file_path
            ),

            "details": details

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not process resume: {str(e)}"
        )


# =========================================================
# GET ALL RESUMES
# =========================================================

@router.get("/all")
def get_all_resumes():

    candidates = []

    if not os.path.exists(UPLOAD_DIR):

        return {
            "count": 0,
            "candidates": []
        }

    try:

        files = os.listdir(
            UPLOAD_DIR
        )

        for filename in files:

            # -------------------------------------------------
            # Only PDF/DOCX files
            # -------------------------------------------------

            extension = os.path.splitext(
                filename
            )[1].lower()

            if extension not in [
                ".pdf",
                ".docx"
            ]:

                continue

            # -------------------------------------------------
            # Only files created by our system
            # Example:
            # user_11_resume.pdf
            # -------------------------------------------------

            if not filename.startswith(
                "user_"
            ):

                continue

            # -------------------------------------------------
            # Extract user ID
            # -------------------------------------------------

            try:

                without_prefix = filename[5:]

                user_id_text = without_prefix.split(
                    "_",
                    1
                )[0]

                user_id = int(
                    user_id_text
                )

            except Exception:

                print(
                    f"Skipping invalid filename: {filename}"
                )

                continue

            file_path = os.path.join(
                UPLOAD_DIR,
                filename
            )

            # -------------------------------------------------
            # Extract details
            # -------------------------------------------------

            details = {}

            if extension == ".pdf":

                try:

                    text = extract_text_from_pdf(
                        file_path
                    )

                    details = extract_candidate_details(
                        text
                    )

                except Exception as e:

                    print(
                        f"AI extraction failed for {filename}: {e}"
                    )

                    details = {}

            # -------------------------------------------------
            # Safety
            # -------------------------------------------------

            if not isinstance(
                details,
                dict
            ):

                details = {}

            # -------------------------------------------------
            # NAME
            # -------------------------------------------------

            name = details.get(
                "name"
            )

            if not name:

                name = "Unknown Candidate"

            # -------------------------------------------------
            # EMAIL
            # -------------------------------------------------

            email = details.get(
                "email"
            )

            if not email:

                email = "No email available"

            # -------------------------------------------------
            # JOB / PROFILE
            # -------------------------------------------------

            job = details.get(
                "job"
            )

            if not job:

                job = details.get(
                    "title"
                )

            if not job:

                # Try candidate profile/title
                job = details.get(
                    "profile"
                )

            if not job:

                job = "Candidate"

            # -------------------------------------------------
            # EXPERIENCE
            # -------------------------------------------------

            experience_data = details.get(
                "experience",
                []
            )

            experience_text = "Fresher"

            if isinstance(
                experience_data,
                list
            ):

                experience_items = []

                for experience in experience_data:

                    if not isinstance(
                        experience,
                        dict
                    ):
                        continue

                    role = experience.get(
                        "role"
                    )

                    company = experience.get(
                        "company"
                    )

                    duration = experience.get(
                        "duration"
                    )

                    if not role:
                        continue

                    role = str(role).strip()

                    if not role:
                        continue

                    item = role

                    if company:

                        item += (
                            f" - {company}"
                        )

                    if duration:

                        item += (
                            f" ({duration})"
                        )

                    experience_items.append(
                        item
                    )

                if experience_items:

                    experience_text = " | ".join(
                        experience_items
                    )

            # -------------------------------------------------
            # RESUME URL
            # -------------------------------------------------

            resume_url = (
                "http://127.0.0.1:8000"
                f"/resume/file/{user_id}"
            )

            # -------------------------------------------------
            # FRONTEND OBJECT
            # -------------------------------------------------

            candidate = {

                "id": user_id,

                "user_id": user_id,

                "name": name,

                "email": email,

                "job": job,

                "experience": experience_text,

                "resumeUrl": resume_url,

                "filename": filename,

                "status": "pending",

                "details": details

            }

            candidates.append(
                candidate
            )

        return {

            "count": len(candidates),

            "candidates": candidates

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not load resumes: {str(e)}"
        )


# =========================================================
# VIEW / DOWNLOAD RESUME
# =========================================================

@router.get("/file/{user_id}")
def view_resume(user_id: int):

    file_path = find_user_resume(
        user_id
    )

    if not file_path:

        raise HTTPException(
            status_code=404,
            detail="Resume file not found"
        )

    filename = os.path.basename(
        file_path
    )

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension == ".pdf":

        media_type = "application/pdf"

    elif extension == ".docx":

        media_type = (
            "application/vnd.openxmlformats-officedocument."
            "wordprocessingml.document"
        )

    else:

        media_type = "application/octet-stream"

    return FileResponse(

        path=file_path,

        filename=filename,

        media_type=media_type

    )