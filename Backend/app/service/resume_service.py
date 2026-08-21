# app/service/resume_service.py

import os
import re
from typing import Any, Dict, Optional

import pdfplumber

from app.service.ai_service import extract_resume_with_ai


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF resume.

    Works with normal text-based PDF resumes.
    Returns an empty string if extraction fails.
    """

    if not pdf_path:
        return ""

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    extracted_pages = []

    try:
        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                try:
                    text = page.extract_text(
                        x_tolerance=2,
                        y_tolerance=3
                    )

                    if text:
                        extracted_pages.append(text)

                except Exception:
                    continue

    except Exception as exc:
        raise RuntimeError(
            f"Unable to read PDF file: {exc}"
        ) from exc

    return "\n".join(extracted_pages).strip()


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_resume_text(text: str) -> str:
    """
    Cleans extracted PDF text without destroying useful information.
    """

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces but preserve lines
    cleaned_lines = []

    for line in text.split("\n"):

        line = re.sub(r"[ \t]+", " ", line)
        line = line.strip()

        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# ============================================================
# RESUME EXTRACTION
# ============================================================

def extract_candidate_details(text: str) -> Dict[str, Any]:
    """
    Main function used by resume routes.

    Sends resume text to the local AI/parser service.
    No OpenAI API is required.
    """

    if not text:
        return {
            "name": None,
            "email": None,
            "phone": None,
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "certifications": [],
            "languages": []
        }

    cleaned_text = clean_resume_text(text)

    try:
        details = extract_resume_with_ai(cleaned_text)

    except Exception as exc:
        print(
            f"Resume extraction error: {exc}"
        )

        details = {
            "name": None,
            "email": None,
            "phone": None,
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "certifications": [],
            "languages": []
        }

    return normalize_candidate_details(details)


# ============================================================
# NORMALIZE RESULT
# ============================================================

def normalize_candidate_details(
    details: Optional[Dict[str, Any]]
) -> Dict[str, Any]:

    if not isinstance(details, dict):
        details = {}

    return {
        "name": details.get("name"),

        "email": details.get("email"),

        "phone": details.get("phone"),

        "skills": _ensure_list(
            details.get("skills")
        ),

        "education": _ensure_list(
            details.get("education")
        ),

        "experience": _ensure_list(
            details.get("experience")
        ),

        "projects": _ensure_list(
            details.get("projects")
        ),

        "certifications": _ensure_list(
            details.get("certifications")
        ),

        "languages": _ensure_list(
            details.get("languages")
        )
    }


# ============================================================
# LIST HELPER
# ============================================================

def _ensure_list(value):

    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [value]


# ============================================================
# COMPLETE PDF -> DETAILS PIPELINE
# ============================================================

def process_resume_pdf(pdf_path: str) -> Dict[str, Any]:
    """
    Complete pipeline:

        PDF
         ↓
        text extraction
         ↓
        text cleaning
         ↓
        resume parser
         ↓
        structured details
    """

    text = extract_text_from_pdf(pdf_path)

    if not text:
        return {
            "text": "",
            "details": normalize_candidate_details({})
        }

    details = extract_candidate_details(text)

    return {
        "text": text,
        "details": details
    }


# ============================================================
# COMPATIBILITY FUNCTIONS
# ============================================================

def extract_resume_details(text: str) -> Dict[str, Any]:
    """
    Compatibility alias.

    Some older routes may use this function name.
    """

    return extract_candidate_details(text)


def parse_resume(text: str) -> Dict[str, Any]:
    """
    Compatibility alias for older code.
    """

    return extract_candidate_details(text)


def analyze_resume(text: str) -> Dict[str, Any]:
    """
    Compatibility alias for older code.
    """

    return extract_candidate_details(text)