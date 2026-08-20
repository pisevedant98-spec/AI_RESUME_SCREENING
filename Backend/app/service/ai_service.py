import re
from typing import List, Dict, Optional


# ============================================================
# GENERIC RESUME AI SERVICE
# ============================================================
#
# This service does NOT use OpenAI.
#
# It is designed for resumes extracted from PDF/DOCX text.
#
# Main goals:
#   1. Correctly identify sections
#   2. Avoid false education detections
#   3. Avoid false experience detections
#   4. Extract projects from project section only
#   5. Extract certifications from certificate section only
#   6. Handle two-column PDF extraction reasonably well
#   7. Work with different resume formats
#
# ============================================================


# ============================================================
# SKILLS DATABASE
# ============================================================

SKILLS = [
    # Programming
    "Python",
    "Java",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "PHP",
    "Ruby",
    "Go",
    "Kotlin",
    "Swift",

    # Web
    "HTML",
    "CSS",
    "React",
    "Angular",
    "Vue",
    "Node.js",
    "Express.js",
    "Django",
    "Flask",
    "FastAPI",

    # Databases
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Oracle",
    "SQLite",
    "DBMS",

    # AI / ML
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "Data Analysis",
    "Natural Language Processing",
    "Computer Vision",

    # Python libraries
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "OpenCV",

    # Cloud / DevOps
    "AWS",
    "Azure",
    "Google Cloud",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",

    # Tools
    "Power BI",
    "Excel",
    "Figma",

    # Other
    "XML",
    "REST API",
    "API",
]


# ============================================================
# LANGUAGE DATABASE
# ============================================================

LANGUAGES = [
    "English",
    "Hindi",
    "Marathi",
    "Tamil",
    "Telugu",
    "Kannada",
    "Malayalam",
    "Gujarati",
    "Bengali",
    "Punjabi",
    "Urdu",
    "French",
    "German",
    "Spanish",
    "Japanese",
    "Chinese",
]


# ============================================================
# SECTION NAMES
# ============================================================

SECTION_ALIASES = {

    "summary": [
        "summary",
        "professional summary",
        "profile",
        "about me",
        "objective",
        "career objective",
        "professional profile"
    ],

    "contact": [
        "contact",
        "contact details",
        "personal details"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship",
        "internships",
        "work history"
    ],

    "education": [
        "education",
        "academic background",
        "academic qualification",
        "qualifications",
        "educational qualification",
        "educational background"
    ],

    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "expertise",
        "technologies",
        "technical expertise",
        "core skills",
        "skills summary"
    ],

    "projects": [
        "projects",
        "project",
        "academic projects",
        "personal projects",
        "key projects",
        "major projects"
    ],

    "certifications": [
        "certifications",
        "certification",
        "certificates",
        "certificate",
        "achievements",
        "awards"
    ],

    "languages": [
        "languages",
        "language"
    ]
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize extracted PDF/DOCX text without destroying
    meaningful line structure.
    """

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\xa0", " ")

    # Normalize unusual bullet characters
    text = text.replace("•", "-")
    text = text.replace("●", "-")
    text = text.replace("▪", "-")
    text = text.replace("◦", "-")

    lines = []

    for line in text.splitlines():

        line = re.sub(r"[ \t]+", " ", line)
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def get_lines(text: str) -> List[str]:

    text = normalize_text(text)

    return [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]


# ============================================================
# BASIC HELPERS
# ============================================================

def clean_value(value: str) -> str:

    if not value:
        return ""

    value = re.sub(r"\s+", " ", value)
    return value.strip(" -|:,")


def unique_list(values):

    result = []

    seen = set()

    for value in values:

        value = clean_value(value)

        if not value:
            continue

        key = value.lower()

        if key not in seen:
            seen.add(key)
            result.append(value)

    return result


# ============================================================
# SECTION DETECTION
# ============================================================

def normalize_section_title(line: str) -> str:

    line = line.lower()

    # Remove bullets
    line = re.sub(r"^[\-\*\•\●\▪\◦]+\s*", "", line)

    # Remove punctuation
    line = re.sub(r"[^a-z ]", "", line)

    line = re.sub(r"\s+", " ", line)

    return line.strip()


def get_section_name(line: str) -> Optional[str]:

    normalized = normalize_section_title(line)

    for section, aliases in SECTION_ALIASES.items():

        for alias in aliases:

            alias_normalized = normalize_section_title(alias)

            if normalized == alias_normalized:
                return section

    return None


def split_sections(lines: List[str]) -> Dict[str, List[str]]:
    """
    Split resume into logical sections.

    IMPORTANT:
    Only lines that exactly resemble section headings
    are treated as section headings.

    This prevents lines such as:
        "Computer Engineering diploma student..."
    from becoming Education.
    """

    sections = {}

    current_section = "header"

    sections[current_section] = []

    for line in lines:

        section = get_section_name(line)

        if section:

            current_section = section

            if current_section not in sections:
                sections[current_section] = []

            continue

        sections.setdefault(current_section, [])
        sections[current_section].append(line)

    return sections


# ============================================================
# EMAIL
# ============================================================

def extract_email(text: str) -> Optional[str]:

    if not text:
        return None

    pattern = (
        r"[A-Za-z0-9._%+\-]+"
        r"@"
        r"[A-Za-z0-9.\-]+"
        r"\."
        r"[A-Za-z]{2,}"
    )

    match = re.search(pattern, text)

    if match:
        return match.group(0).lower()

    return None


# ============================================================
# PHONE
# ============================================================

def extract_phone(text: str) -> Optional[str]:

    if not text:
        return None

    # +91 98765 43210
    match = re.search(
        r"(?:\+91|91)[\s\-]*"
        r"([6-9]\d{4})[\s\-]*"
        r"(\d{5})",
        text
    )

    if match:
        return match.group(1) + match.group(2)

    # 98765 43210
    match = re.search(
        r"(?<!\d)"
        r"([6-9]\d{4})"
        r"[\s\-]*"
        r"(\d{5})"
        r"(?!\d)",
        text
    )

    if match:
        return match.group(1) + match.group(2)

    return None


# ============================================================
# NAME
# ============================================================

def is_name_candidate(value: str) -> bool:

    value = clean_value(value)

    if not value:
        return False

    if len(value) < 3 or len(value) > 60:
        return False

    if "@" in value:
        return False

    if re.search(r"\d", value):
        return False

    # Avoid obvious headings
    invalid = {
        "resume",
        "curriculum vitae",
        "cv",
        "contact",
        "contact details",
        "experience",
        "education",
        "skills",
        "expertise",
        "projects",
        "certificates",
        "certifications",
        "languages",
        "summary",
        "profile",
        "objective"
    }

    if value.lower() in invalid:
        return False

    return bool(
        re.fullmatch(
            r"[A-Za-z][A-Za-z .'\-]{2,59}",
            value
        )
    )


def extract_name(text: str) -> Optional[str]:

    lines = get_lines(text)

    # Explicit Name:
    for line in lines[:20]:

        match = re.match(
            r"^(?:name|full name)\s*[:\-]\s*(.+)$",
            line,
            re.IGNORECASE
        )

        if match:

            candidate = clean_value(match.group(1))

            if is_name_candidate(candidate):
                return candidate

    # Usually the first strong name-like line
    for line in lines[:12]:

        candidate = clean_value(line)

        if not is_name_candidate(candidate):
            continue

        # Job titles are not names
        lower = candidate.lower()

        job_words = [
            "engineer",
            "developer",
            "intern",
            "student",
            "manager",
            "designer",
            "analyst",
            "consultant",
            "specialist",
            "administrator"
        ]

        if any(word in lower for word in job_words):
            continue

        return candidate

    return None


# ============================================================
# SKILLS
# ============================================================

def extract_skills(text: str) -> List[str]:

    if not text:
        return []

    lines = get_lines(text)
    sections = split_sections(lines)

    # Prefer Skills section.
    search_parts = []

    if "skills" in sections:
        search_parts.extend(sections["skills"])

    # Also use full resume because many resumes mention
    # technologies inside project descriptions.
    search_parts.extend(lines)

    search_text = "\n".join(search_parts)

    found = []

    for skill in SKILLS:

        # C is intentionally NOT included as a normal skill.
        # This prevents random "C" matches.
        if skill == "C":
            continue

        pattern = (
            r"(?<![A-Za-z0-9+#])"
            + re.escape(skill)
            + r"(?![A-Za-z0-9+#])"
        )

        if re.search(
            pattern,
            search_text,
            re.IGNORECASE
        ):

            found.append(skill)

    # Remove duplicates
    return unique_list(found)


# ============================================================
# YEAR / DATE HELPERS
# ============================================================

YEAR_PATTERN = re.compile(
    r"\b(?:19|20)\d{2}\b"
)

YEAR_RANGE_PATTERN = re.compile(
    r"\b(?:19|20)\d{2}\s*[-–]\s*(?:19|20)\d{2}\b"
)


def extract_year_range(text: str) -> Optional[str]:

    if not text:
        return None

    match = YEAR_RANGE_PATTERN.search(text)

    if match:
        return clean_value(match.group(0))

    years = YEAR_PATTERN.findall(text)

    if len(years) >= 2:

        return f"{years[0]} - {years[1]}"

    if len(years) == 1:
        return years[0]

    return None


def extract_percentage(text: str) -> Optional[str]:

    match = re.search(
        r"\b\d{1,3}(?:\.\d+)?\s*%",
        text
    )

    if match:
        return match.group(0).replace(" ", "")

    return None


# ============================================================
# EDUCATION
# ============================================================

EDUCATION_DEGREE_PATTERNS = [

    (
        "Diploma",
        r"\bdiploma\s+(?:in\s+)?"
        r"[A-Za-z& ]{2,80}"
    ),

    (
        "B.Tech",
        r"\bb\.?\s*tech\b"
    ),

    (
        "B.E",
        r"\bb\.?\s*e\.?\b"
    ),

    (
        "M.Tech",
        r"\bm\.?\s*tech\b"
    ),

    (
        "M.E",
        r"\bm\.?\s*e\.?\b"
    ),

    (
        "BCA",
        r"\bbca\b"
    ),

    (
        "MCA",
        r"\bmca\b"
    ),

    (
        "B.Sc",
        r"\bb\.?\s*sc\b"
    ),

    (
        "M.Sc",
        r"\bm\.?\s*sc\b"
    ),

    (
        "BBA",
        r"\bbba\b"
    ),

    (
        "MBA",
        r"\bmba\b"
    ),

    (
        "Bachelor",
        r"\bbachelor(?:'s)?\b"
    ),

    (
        "Master",
        r"\bmaster(?:'s)?\b"
    ),

    (
        "SSC",
        r"\bssc\b"
    ),

    (
        "HSC",
        r"\bhsc\b"
    )
]


def looks_like_education_line(line: str) -> bool:

    lower = line.lower()

    # A real education line should contain one of these.
    degree_words = [
        "diploma",
        "b.tech",
        "btech",
        "b.e",
        "b.e.",
        "m.tech",
        "mtech",
        "m.e",
        "m.e.",
        "bca",
        "mca",
        "b.sc",
        "m.sc",
        "bba",
        "mba",
        "bachelor",
        "master",
        "ssc",
        "hsc",
        "secondary",
        "school",
        "polytechnic",
        "college",
        "university",
        "degree"
    ]

    if not any(word in lower for word in degree_words):
        return False

    # CRITICAL:
    # Do not treat summary sentences as education.
    bad_phrases = [
        "diploma student with",
        "student with",
        "internship experience",
        "hands-on experience",
        "skilled in",
        "strong problem",
        "passion for"
    ]

    if any(phrase in lower for phrase in bad_phrases):
        return False

    return True


def build_education_entry(
    line: str,
    nearby_lines: List[str]
) -> Optional[Dict]:

    if not looks_like_education_line(line):
        return None

    combined = " ".join(
        [line] + nearby_lines
    )

    combined = clean_value(combined)

    # Degree
    degree = None

    for label, pattern in EDUCATION_DEGREE_PATTERNS:

        match = re.search(
            pattern,
            line,
            re.IGNORECASE
        )

        if match:

            if label == "Diploma":

                degree = clean_value(
                    match.group(0)
                )

                # Stop degree from swallowing a huge sentence.
                degree = re.sub(
                    r"\s+Percentage.*$",
                    "",
                    degree,
                    flags=re.IGNORECASE
                )

            else:
                degree = label

            break

    if not degree:
        return None

    # Year
    year = extract_year_range(combined)

    # Percentage
    percentage = extract_percentage(combined)

    # Institution
    institution = None

    institution_patterns = [
        r"([A-Z][A-Za-z .&'-]*(?:Polytechnic|College|University|School|Institute|Institution)[A-Za-z .,&'-]*)",
        r"([A-Z][A-Za-z .&'-]+,\s*[A-Z][A-Za-z .&'-]+)"
    ]

    for pattern in institution_patterns:

        match = re.search(
            pattern,
            combined,
            re.IGNORECASE
        )

        if match:

            candidate = clean_value(
                match.group(1)
            )

            # Remove obvious junk
            candidate = re.sub(
                r"\s+Percentage.*$",
                "",
                candidate,
                flags=re.IGNORECASE
            )

            if len(candidate) >= 4:
                institution = candidate
                break

    return {
        "degree": degree,
        "year": year,
        "institution": institution,
        "percentage": percentage
    }


def extract_education(text: str) -> List[Dict]:

    lines = get_lines(text)
    sections = split_sections(lines)

    education_lines = sections.get(
        "education",
        []
    )

    # If an Education heading exists, ONLY parse its section.
    # This is the most important protection against false detections.
    if education_lines:

        candidates = education_lines

    else:

        # Fallback: search for very strong degree lines only.
        candidates = []

        for line in lines:

            lower = line.lower()

            strong_patterns = [
                "diploma in ",
                "b.tech",
                "btech",
                "b.e.",
                "m.tech",
                "mtech",
                "bca",
                "mca",
                "b.sc",
                "m.sc",
                "mba",
                "bba",
                "ssc",
                "hsc"
            ]

            if any(
                pattern in lower
                for pattern in strong_patterns
            ):

                if looks_like_education_line(line):
                    candidates.append(line)

    results = []

    for i, line in enumerate(candidates):

        nearby = candidates[
            i + 1:i + 3
        ]

        entry = build_education_entry(
            line,
            nearby
        )

        if entry:

            # Prevent duplicate degrees
            duplicate = False

            for existing in results:

                if (
                    existing["degree"].lower()
                    == entry["degree"].lower()
                    and
                    existing.get("year")
                    == entry.get("year")
                ):
                    duplicate = True
                    break

            if not duplicate:
                results.append(entry)

    return results[:10]


# ============================================================
# EXPERIENCE
# ============================================================

JOB_TITLE_WORDS = [
    "intern",
    "developer",
    "engineer",
    "designer",
    "analyst",
    "manager",
    "consultant",
    "administrator",
    "programmer",
    "specialist",
    "trainee",
    "associate"
]


def looks_like_job_title(line: str) -> bool:

    lower = line.lower()

    return any(
        re.search(
            r"\b" + re.escape(word) + r"\b",
            lower
        )
        for word in JOB_TITLE_WORDS
    )


def looks_like_company(line: str) -> bool:

    lower = line.lower()

    company_words = [
        "pvt",
        "private",
        "ltd",
        "limited",
        "technologies",
        "technology",
        "solutions",
        "systems",
        "software",
        "services",
        "company",
        "inc",
        "llp",
        "itvedant",
        "jalgi"
    ]

    return any(
        word in lower
        for word in company_words
    )


def extract_experience(text: str) -> List[Dict]:

    lines = get_lines(text)
    sections = split_sections(lines)

    experience_lines = sections.get(
        "experience",
        []
    )

    # If Experience section exists, ONLY use it.
    if not experience_lines:
        return []

    results = []

    i = 0

    while i < len(experience_lines):

        line = experience_lines[i]

        year = extract_year_range(line)

        # A job title normally contains an internship/job word.
        if looks_like_job_title(line):

            role = clean_value(line)

            # Remove date from role
            role = YEAR_RANGE_PATTERN.sub(
                "",
                role
            )

            role = clean_value(role)

            company = None

            # Search next few lines for company.
            for j in range(
                i + 1,
                min(
                    i + 5,
                    len(experience_lines)
                )
            ):

                candidate = experience_lines[j]

                if looks_like_company(candidate):

                    company = clean_value(
                        candidate
                    )

                    # Remove date
                    company = YEAR_RANGE_PATTERN.sub(
                        "",
                        company
                    )

                    company = clean_value(
                        company
                    )

                    break

            # If company is on same line
            if not company:

                same_line_match = re.search(
                    r"(?:at|@)\s+(.+)$",
                    role,
                    re.IGNORECASE
                )

                if same_line_match:

                    company = clean_value(
                        same_line_match.group(1)
                    )

            # Ignore generic job-like sentences
            if (
                role
                and
                len(role) <= 100
                and
                not re.search(
                    r"student|experience with|hands-on|"
                    r"problem-solving|passion|skills",
                    role,
                    re.IGNORECASE
                )
            ):

                results.append({
                    "role": role,
                    "company": company,
                    "duration": year
                })

        i += 1

    # Remove duplicate entries
    cleaned = []

    seen = set()

    for item in results:

        key = (
            item["role"].lower(),
            (item["company"] or "").lower(),
            item["duration"] or ""
        )

        if key not in seen:

            seen.add(key)
            cleaned.append(item)

    return cleaned[:10]


# ============================================================
# PROJECTS
# ============================================================

def is_project_candidate(line: str) -> bool:

    line = clean_value(line)

    if not line:
        return False

    lower = line.lower()

    # Ignore obvious noise
    bad = [
        "percentage:",
        "completed a",
        "internship",
        "experience",
        "successfully presented",
        "participation certificate",
        "contact",
        "phone",
        "email",
        "address"
    ]

    if any(
        phrase in lower
        for phrase in bad
    ):
        return False

    # Project lines usually aren't extremely long.
    if len(line) > 180:
        return False

    return True


def extract_projects(text: str) -> List[str]:

    lines = get_lines(text)
    sections = split_sections(lines)

    project_lines = sections.get(
        "projects",
        []
    )

    # ONLY use actual Projects section.
    # Never guess projects from the whole resume.
    if not project_lines:
        return []

    projects = []

    for line in project_lines:

        line = clean_value(line)

        # Remove bullet
        line = re.sub(
            r"^[\-\*\•\●\▪\◦]+\s*",
            "",
            line
        )

        if not is_project_candidate(line):
            continue

        projects.append(line)

    return unique_list(projects)[:20]


# ============================================================
# CERTIFICATIONS
# ============================================================

def extract_certifications(text: str) -> List[str]:

    lines = get_lines(text)
    sections = split_sections(lines)

    certificate_lines = sections.get(
        "certifications",
        []
    )

    if not certificate_lines:
        return []

    results = []

    for line in certificate_lines:

        line = clean_value(line)

        lower = line.lower()

        # Ignore section noise
        if lower in {
            "certificates",
            "certification",
            "certifications"
        }:
            continue

        # Ignore generic sentence fragments
        if len(line) < 4:
            continue

        # Remove obvious project leakage
        if "project management" == lower:
            continue

        results.append(line)

    return unique_list(results)[:20]


# ============================================================
# LANGUAGES
# ============================================================

def extract_languages(text: str) -> List[str]:

    lines = get_lines(text)
    sections = split_sections(lines)

    # Prefer language section
    language_lines = sections.get(
        "languages",
        []
    )

    if language_lines:

        search_text = " ".join(
            language_lines
        )

    else:

        # Fallback to only lines near a Languages heading.
        search_text = ""

        for i, line in enumerate(lines):

            if get_section_name(line) == "languages":

                search_text = " ".join(
                    lines[i + 1:i + 10]
                )

                break

    found = []

    for language in LANGUAGES:

        if re.search(
            r"(?<![A-Za-z])"
            + re.escape(language)
            + r"(?![A-Za-z])",
            search_text,
            re.IGNORECASE
        ):

            found.append(language)

    return found


# ============================================================
# FALLBACK LANGUAGE EXTRACTION
# ============================================================

def extract_languages_from_resume(text: str) -> List[str]:

    lines = get_lines(text)

    for i, line in enumerate(lines):

        normalized = normalize_section_title(
            line
        )

        if normalized in {
            "language",
            "languages"
        }:

            nearby_text = " ".join(
                lines[i + 1:i + 8]
            )

            found = []

            for language in LANGUAGES:

                if re.search(
                    r"(?<![A-Za-z])"
                    + re.escape(language)
                    + r"(?![A-Za-z])",
                    nearby_text,
                    re.IGNORECASE
                ):

                    found.append(language)

            if found:
                return found

    return []


# ============================================================
# FINAL CLEANUP
# ============================================================

def clean_education(items):

    result = []

    for item in items:

        if not item:
            continue

        degree = clean_value(
            item.get("degree", "")
        )

        # Remove obvious false positives
        bad = [
            "student with",
            "internship experience",
            "hands-on experience",
            "skilled in",
            "problem-solving",
            "passion for"
        ]

        if any(
            phrase in degree.lower()
            for phrase in bad
        ):
            continue

        if len(degree) > 100:
            continue

        result.append({
            "degree": degree,
            "year": item.get("year"),
            "institution": item.get("institution"),
            "percentage": item.get("percentage")
        })

    return result


def clean_experience(items):

    result = []

    seen = set()

    for item in items:

        role = clean_value(
            item.get("role", "")
        )

        company = clean_value(
            item.get("company") or ""
        )

        duration = clean_value(
            item.get("duration") or ""
        )

        if not role:
            continue

        # Reject summary sentences
        if re.search(
            r"student with|hands-on experience|"
            r"strong problem|passion for|"
            r"skilled in",
            role,
            re.IGNORECASE
        ):
            continue

        key = (
            role.lower(),
            company.lower(),
            duration.lower()
        )

        if key in seen:
            continue

        seen.add(key)

        result.append({
            "role": role,
            "company": company or None,
            "duration": duration or None
        })

    return result


# ============================================================
# MAIN EXTRACTION FUNCTION
# ============================================================

def extract_resume_with_ai(text: str) -> Dict:

    """
    Main function used by the resume service.

    No OpenAI.
    No external API.
    No API key.

    Returns structured resume information.
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

    cleaned_text = normalize_text(text)

    # --------------------------------------------------------
    # Extract
    # --------------------------------------------------------

    details = {

        "name": extract_name(
            cleaned_text
        ),

        "email": extract_email(
            cleaned_text
        ),

        "phone": extract_phone(
            cleaned_text
        ),

        "skills": extract_skills(
            cleaned_text
        ),

        "education": extract_education(
            cleaned_text
        ),

        "experience": extract_experience(
            cleaned_text
        ),

        "projects": extract_projects(
            cleaned_text
        ),

        "certifications": extract_certifications(
            cleaned_text
        ),

        "languages": extract_languages(
            cleaned_text
        )
    }

    # --------------------------------------------------------
    # Language fallback
    # --------------------------------------------------------

    if not details["languages"]:

        details["languages"] = (
            extract_languages_from_resume(
                cleaned_text
            )
        )

    # --------------------------------------------------------
    # Final cleanup
    # --------------------------------------------------------

    details["education"] = clean_education(
        details["education"]
    )

    details["experience"] = clean_experience(
        details["experience"]
    )

    details["skills"] = unique_list(
        details["skills"]
    )

    details["projects"] = unique_list(
        details["projects"]
    )

    details["certifications"] = unique_list(
        details["certifications"]
    )

    details["languages"] = unique_list(
        details["languages"]
    )

    return details


# ============================================================
# COMPATIBILITY ALIAS
# ============================================================

def extract_candidate_details(text: str) -> Dict:
    """
    Compatibility function.

    If your existing resume_service.py imports:
        extract_candidate_details

    it will continue working.
    """

    return extract_resume_with_ai(text)


# ============================================================
# OPTIONAL COMPLETE PROCESSOR
# ============================================================

def process_resume_text(text: str) -> Dict:

    cleaned_text = normalize_text(text)

    return {
        "text": cleaned_text,
        "details": extract_resume_with_ai(
            cleaned_text
        )
    }