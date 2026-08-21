# app/service/ai_service.py

import re
from typing import Any, Dict, List, Optional


# ============================================================
# LOCAL RESUME AI / NLP SERVICE
# ============================================================
# No OpenAI
# No API
# No internet
#
# This parser is designed to work with messy PDF text extraction.
# It uses section detection + patterns + scoring instead of simply
# searching keywords everywhere.
# ============================================================


# ============================================================
# SKILLS DATABASE
# ============================================================

SKILLS = [
    # Programming languages
    "Python",
    "Java",
    "C++",
    "C#",
    "C",
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
    "Bootstrap",
    "Tailwind",

    # Python frameworks
    "Django",
    "Flask",
    "FastAPI",

    # Databases
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQLite",
    "Oracle",
    "DBMS",

    # AI / ML / Data
    "Artificial Intelligence",
    "AI",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "Data Analysis",
    "NLP",
    "Computer Vision",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",

    # Cloud / DevOps
    "AWS",
    "Azure",
    "Google Cloud",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "GitLab",

    # Other
    "Power BI",
    "Excel",
    "XML",
    "JSON",
    "REST API",
    "REST",
    "API",
]


# ============================================================
# LANGUAGES
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
    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship",
        "internships",
        "work history",
        "career history",
    },

    "education": {
        "education",
        "academic background",
        "academic qualification",
        "qualifications",
        "educational qualification",
        "educational background",
    },

    "projects": {
        "projects",
        "project",
        "academic projects",
        "personal projects",
        "major projects",
    },

    "certifications": {
        "certificates",
        "certificate",
        "certifications",
        "certification",
        "achievements",
        "awards",
    },

    "skills": {
        "skills",
        "technical skills",
        "technical expertise",
        "expertise",
        "technologies",
        "technical knowledge",
        "competencies",
    },

    "languages": {
        "language",
        "languages",
        "known languages",
    },

    "contact": {
        "contact",
        "contact details",
        "personal details",
    },

    "summary": {
        "summary",
        "profile",
        "professional summary",
        "career objective",
        "objective",
        "about me",
    },
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # PDF extraction sometimes produces weird spacing.
    text = text.replace("\u00a0", " ")
    text = text.replace("\u200b", "")

    return text


def clean_line(line: str) -> str:
    if not line:
        return ""

    line = line.replace("\u00a0", " ")
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def get_lines(text: str) -> List[str]:
    text = normalize_text(text)

    lines = []

    for raw in text.split("\n"):
        line = clean_line(raw)

        if line:
            lines.append(line)

    return lines


def normalize_for_compare(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


# ============================================================
# SECTION DETECTION
# ============================================================

def detect_section(line: str) -> Optional[str]:
    """
    Detect only genuine section headings.

    Important:
    We DON'T classify a line as a section just because it contains
    a keyword. It must closely match the heading.
    """

    normalized = normalize_for_compare(line)

    if not normalized:
        return None

    for section, aliases in SECTION_ALIASES.items():

        for alias in aliases:

            alias_normalized = normalize_for_compare(alias)

            if normalized == alias_normalized:
                return section

    return None


def split_sections(text: str) -> Dict[str, List[str]]:
    """
    Split resume into logical sections.

    This is the main protection against:
    - education appearing as experience
    - projects appearing as certifications
    - languages appearing as projects
    """

    lines = get_lines(text)

    sections = {
        "header": [],
        "summary": [],
        "contact": [],
        "experience": [],
        "education": [],
        "projects": [],
        "certifications": [],
        "skills": [],
        "languages": [],
        "other": [],
    }

    current = "header"

    for line in lines:

        section = detect_section(line)

        if section:
            current = section
            continue

        sections.setdefault(current, [])
        sections[current].append(line)

    return sections


# ============================================================
# GENERIC HELPERS
# ============================================================

def unique_list(items: List[Any]) -> List[Any]:

    result = []
    seen = set()

    for item in items:

        if isinstance(item, str):
            key = normalize_for_compare(item)
        else:
            key = str(item)

        if key and key not in seen:
            seen.add(key)
            result.append(item)

    return result


def contains_year(text: str) -> bool:
    return bool(
        re.search(
            r"\b(?:19|20)\d{2}\b",
            text
        )
    )


def extract_year_range(text: str) -> Optional[str]:

    match = re.search(
        r"\b((?:19|20)\d{2})\s*[-–—]\s*((?:19|20)\d{2}|Present|Current)\b",
        text,
        re.IGNORECASE
    )

    if match:
        return f"{match.group(1)} - {match.group(2)}"

    match = re.search(
        r"\b((?:19|20)\d{2})\b",
        text
    )

    if match:
        return match.group(1)

    return None


def extract_percentage(text: str) -> Optional[str]:

    match = re.search(
        r"(\d{1,3}(?:\.\d+)?)\s*%",
        text
    )

    if match:
        return f"{match.group(1)}%"

    return None


def remove_year(text: str) -> str:

    text = re.sub(
        r"\b(?:19|20)\d{2}\s*[-–—]\s*(?:19|20)?\d{2}\b",
        "",
        text
    )

    text = re.sub(
        r"\b(?:19|20)\d{2}\b",
        "",
        text
    )

    return clean_line(text)


# ============================================================
# NAME
# ============================================================

def extract_name(text: str) -> Optional[str]:

    lines = get_lines(text)

    if not lines:
        return None

    # Explicit name label
    for line in lines[:20]:

        match = re.match(
            r"^(?:name|full name)\s*[:\-]\s*(.+)$",
            line,
            re.IGNORECASE
        )

        if match:
            candidate = clean_line(match.group(1))

            if candidate:
                return candidate

    ignored = {
        "resume",
        "curriculum vitae",
        "cv",
        "profile",
        "summary",
        "objective",
        "contact",
        "contact details",
        "experience",
        "education",
        "projects",
        "skills",
        "expertise",
        "certificates",
        "certifications",
        "languages",
    }

    candidates = []

    for index, line in enumerate(lines[:20]):

        lower = line.lower()

        if lower in ignored:
            continue

        if "@" in line:
            continue

        if re.search(r"\d{5,}", line):
            continue

        if detect_section(line):
            continue

        # Do not accept obvious job titles.
        if any(
            word in lower
            for word in [
                "engineer",
                "developer",
                "intern",
                "student",
                "manager",
                "designer",
                "analyst",
                "consultant",
                "specialist",
            ]
        ):
            continue

        if re.fullmatch(
            r"[A-Za-z][A-Za-z .'\-]{2,60}",
            line
        ):
            words = line.split()

            if 1 <= len(words) <= 5:

                score = 0

                if index == 0:
                    score += 10

                if len(words) >= 2:
                    score += 5

                if line.isupper():
                    score += 5

                candidates.append(
                    (score, line)
                )

    if candidates:
        candidates.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return candidates[0][1]

    return None


# ============================================================
# EMAIL
# ============================================================

def extract_email(text: str) -> Optional[str]:

    match = re.search(
        r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}",
        text
    )

    if match:
        return match.group(0).lower()

    return None


# ============================================================
# PHONE
# ============================================================

def extract_phone(text: str) -> Optional[str]:

    patterns = [
        r"(?:\+91[\s\-]*)?([6-9]\d{4})[\s\-]?(\d{5})",
        r"(?:\+91[\s\-]*)?([6-9]\d{2})[\s\-]?(\d{3})[\s\-]?(\d{4})",
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            digits = "".join(match.groups())

            if len(digits) == 10:
                return digits

    return None


# ============================================================
# SKILLS
# ============================================================

def extract_skills(text: str) -> List[str]:

    sections = split_sections(text)

    # Skills section gets priority.
    skill_text = " ".join(
        sections.get("skills", [])
    )

    # Also use full text as fallback because many PDF layouts
    # don't preserve the original columns.
    search_text = (
        skill_text
        if skill_text
        else text
    )

    found = []

    # Longer skills first.
    ordered_skills = sorted(
        SKILLS,
        key=len,
        reverse=True
    )

    for skill in ordered_skills:

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

    # Remove duplicate variants.
    result = []

    seen = set()

    for skill in found:

        key = normalize_for_compare(skill)

        if key not in seen:
            seen.add(key)
            result.append(skill)

    return result


# ============================================================
# EDUCATION
# ============================================================

DEGREE_PATTERNS = [
    r"\bph\.?d\b",
    r"\bdoctorate\b",
    r"\bm\.?tech\b",
    r"\bmtech\b",
    r"\bm\.?e\b",
    r"\bmaster(?:'s)?\b",
    r"\bmca\b",
    r"\bmba\b",
    r"\bm\.?sc\b",
    r"\bb\.?tech\b",
    r"\bbtech\b",
    r"\bb\.?e\b",
    r"\bbachelor(?:'s)?\b",
    r"\bbca\b",
    r"\bbba\b",
    r"\bb\.?sc\b",
    r"\bdiploma\b",
    r"\bssc\b",
    r"\bhsc\b",
    r"\b10th\b",
    r"\b12th\b",
    r"\bhigher secondary\b",
]


def looks_like_education(line: str) -> bool:

    lower = line.lower()

    return any(
        re.search(pattern, lower)
        for pattern in DEGREE_PATTERNS
    )


def find_institution(lines: List[str], index: int) -> Optional[str]:

    candidates = []

    start = max(0, index - 2)
    end = min(len(lines), index + 4)

    for i in range(start, end):

        if i == index:
            continue

        line = lines[i]

        lower = line.lower()

        if "percentage" in lower:
            continue

        if re.search(r"\b(?:19|20)\d{2}\b", line):
            continue

        if "@" in line:
            continue

        # Strong institution indicators.
        if any(
            word in lower
            for word in [
                "university",
                "college",
                "school",
                "polytechnic",
                "institute",
                "academy",
            ]
        ):
            candidates.append(line)

    if candidates:
        return candidates[0]

    return None


def extract_education(text: str) -> List[Dict[str, Optional[str]]]:

    sections = split_sections(text)

    lines = sections.get("education", [])

    # If a clean education section exists, use it.
    # Otherwise find lines that look strongly educational.
    if not lines:

        all_lines = get_lines(text)

        lines = [
            line
            for line in all_lines
            if looks_like_education(line)
        ]

    results = []

    i = 0

    while i < len(lines):

        line = lines[i]

        if not looks_like_education(line):
            i += 1
            continue

        # Reject sentences that merely mention education.
        lower = line.lower()

        if (
            len(line.split()) > 10
            and not re.search(
                r"\b(?:diploma|degree|ssc|hsc|btech|b\.tech|mtech|m\.tech|bca|mca)\b",
                lower
            )
        ):
            i += 1
            continue

        year = extract_year_range(line)

        percentage = extract_percentage(line)

        degree = remove_year(line)

        degree = re.sub(
            r"\bpercentage\s*:\s*[\d.]+\s*%",
            "",
            degree,
            flags=re.IGNORECASE
        )

        degree = clean_line(degree)

        # Sometimes year and percentage are on nearby lines.
        nearby = lines[i:i + 4]

        for nearby_line in nearby:

            if not year:
                year = extract_year_range(
                    nearby_line
                )

            if not percentage:
                percentage = extract_percentage(
                    nearby_line
                )

        institution = find_institution(
            lines,
            i
        )

        # Remove accidental institution fragments.
        if institution:
            institution = clean_line(institution)

        # Valid education entries must have a real degree keyword.
        if not looks_like_education(degree):
            i += 1
            continue

        results.append({
            "degree": degree,
            "year": year,
            "institution": institution,
            "percentage": percentage,
        })

        i += 1

    # Deduplicate.
    final = []

    seen = set()

    for item in results:

        key = (
            normalize_for_compare(
                item["degree"] or ""
            ),
            item["year"] or "",
            normalize_for_compare(
                item["institution"] or ""
            ),
        )

        if key not in seen:
            seen.add(key)
            final.append(item)

    return final[:10]


# ============================================================
# EXPERIENCE
# ============================================================

EXPERIENCE_ROLE_WORDS = [
    "intern",
    "developer",
    "engineer",
    "designer",
    "analyst",
    "manager",
    "consultant",
    "administrator",
    "specialist",
    "trainee",
    "associate",
    "executive",
    "architect",
]


def looks_like_experience_role(line: str) -> bool:

    lower = line.lower()

    return any(
        word in lower
        for word in EXPERIENCE_ROLE_WORDS
    )


def find_company(lines: List[str], index: int) -> Optional[str]:

    candidates = []

    start = max(0, index - 2)
    end = min(len(lines), index + 5)

    for i in range(start, end):

        if i == index:
            continue

        line = lines[i]
        lower = line.lower()

        # Never treat contact data as company.
        if "@" in line:
            continue

        if re.search(
            r"\b(?:phone|email|address)\b",
            lower
        ):
            continue

        if re.search(
            r"\b\d{10}\b",
            line
        ):
            continue

        # Education shouldn't become company.
        if looks_like_education(line):
            continue

        # Company indicators.
        if any(
            token in lower
            for token in [
                "pvt",
                "private",
                "ltd",
                "limited",
                "technologies",
                "technology",
                "solutions",
                "systems",
                "software",
                "company",
                "corporation",
                "inc",
                "llp",
                "itvedant",
            ]
        ):
            candidates.append(line)

    if candidates:
        return candidates[0]

    return None


def extract_experience(text: str) -> List[Dict[str, Optional[str]]]:

    sections = split_sections(text)

    lines = sections.get("experience", [])

    # If there is no experience section, don't scan the whole resume
    # aggressively. This avoids education/projects becoming experience.
    if not lines:
        return []

    results = []

    i = 0

    while i < len(lines):

        line = lines[i]

        year = extract_year_range(line)

        # A role is strongest when it contains an experience role word.
        role_match = looks_like_experience_role(line)

        if not role_match:
            i += 1
            continue

        # Reject generic sentences.
        if len(line.split()) > 12:
            i += 1
            continue

        role = remove_year(line)

        role = clean_line(role)

        # Remove obvious junk from role.
        role = re.sub(
            r"^(?:phone|email|address)\s+",
            "",
            role,
            flags=re.IGNORECASE
        )

        if not role:
            i += 1
            continue

        company = find_company(
            lines,
            i
        )

        # Search nearby lines for duration.
        if not year:

            for nearby in lines[i:i + 4]:

                possible_year = extract_year_range(
                    nearby
                )

                if possible_year:
                    year = possible_year
                    break

        results.append({
            "role": role,
            "company": company,
            "duration": year,
        })

        i += 1

    # Deduplicate.
    final = []

    seen = set()

    for item in results:

        key = (
            normalize_for_compare(
                item["role"] or ""
            ),
            normalize_for_compare(
                item["company"] or ""
            ),
            item["duration"] or "",
        )

        if key not in seen:
            seen.add(key)
            final.append(item)

    return final[:15]


# ============================================================
# PROJECTS
# ============================================================

def looks_like_project(line: str) -> bool:

    lower = line.lower()

    if not line:
        return False

    # Project names usually aren't headings, contact data,
    # education or certificate lines.
    forbidden = [
        "english",
        "hindi",
        "marathi",
        "certificates",
        "certificate",
        "certification",
        "education",
        "experience",
        "skills",
        "percentage",
        "phone",
        "email",
        "address",
    ]

    if lower in forbidden:
        return False

    if "@" in line:
        return False

    if re.search(r"\b\d{10}\b", line):
        return False

    if looks_like_education(line):
        return False

    if "%" in line:
        return False

    return True


def extract_projects(text: str) -> List[str]:

    sections = split_sections(text)

    lines = sections.get("projects", [])

    if not lines:
        return []

    projects = []

    for line in lines:

        if not looks_like_project(line):
            continue

        # Avoid section headings accidentally included.
        if detect_section(line):
            continue

        # A project usually has reasonable length.
        if len(line) < 3:
            continue

        if len(line) > 150:
            continue

        projects.append(line)

    return unique_list(projects)[:20]


# ============================================================
# CERTIFICATIONS
# ============================================================

def extract_certifications(text: str) -> List[str]:

    sections = split_sections(text)

    lines = sections.get("certifications", [])

    if not lines:
        return []

    results = []

    for line in lines:

        if not line:
            continue

        if detect_section(line):
            continue

        # Don't treat generic certificate words as certificates.
        if normalize_for_compare(line) in {
            "certificate",
            "certificates",
            "certification",
            "certifications",
        }:
            continue

        results.append(line)

    return unique_list(results)[:20]


# ============================================================
# LANGUAGES
# ============================================================

def extract_languages(text: str) -> List[str]:

    sections = split_sections(text)

    section_text = " ".join(
        sections.get("languages", [])
    )

    # If language section exists, trust it.
    # Otherwise use full text only for known languages.
    search_text = (
        section_text
        if section_text
        else text
    )

    found = []

    for language in LANGUAGES:

        pattern = (
            r"(?<![A-Za-z])"
            + re.escape(language)
            + r"(?![A-Za-z])"
        )

        if re.search(
            pattern,
            search_text,
            re.IGNORECASE
        ):
            found.append(language)

    return unique_list(found)


# ============================================================
# SUMMARY
# ============================================================

def extract_summary(text: str) -> Optional[str]:

    sections = split_sections(text)

    lines = sections.get("summary", [])

    if not lines:
        return None

    value = " ".join(lines)

    value = clean_line(value)

    return value if value else None


# ============================================================
# MAIN EXTRACTION
# ============================================================

def extract_resume_with_ai(text: str) -> Dict[str, Any]:

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
            "languages": [],
        }

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "projects": extract_projects(text),
        "certifications": extract_certifications(text),
        "languages": extract_languages(text),
    }


# ============================================================
# COMPATIBILITY ALIASES
# ============================================================

def extract_candidate_details(text: str) -> Dict[str, Any]:
    """
    Compatibility function used by resume_service.py / routes.
    """

    return extract_resume_with_ai(text)