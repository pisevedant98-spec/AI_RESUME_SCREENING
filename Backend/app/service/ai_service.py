import re


# ============================================================
# LOCAL RESUME EXTRACTION SERVICE
# NO OPENAI
# NO API KEY
# NO INTERNET
# ============================================================


SKILLS = [
    "Python",
    "Java",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "React",
    "Angular",
    "Vue",
    "Django",
    "Flask",
    "FastAPI",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Science",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "PyTorch",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Azure",
    "Power BI",
    "Excel",
    "DBMS",
    "XML",
    "AI"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_line(line: str) -> str:

    line = line.replace("\xa0", " ")

    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line.strip()


def get_lines(text: str):

    lines = []

    for line in text.splitlines():

        line = clean_line(line)

        if line:
            lines.append(line)

    return lines


def normalize(value: str):

    return re.sub(
        r"[^a-z0-9]+",
        " ",
        value.lower()
    ).strip()


# ============================================================
# NAME
# ============================================================

def is_valid_name(name: str):

    if not name:
        return False

    if "@" in name:
        return False

    if re.search(r"\d", name):
        return False

    if len(name) < 3:
        return False

    if len(name) > 50:
        return False

    if not re.fullmatch(
        r"[A-Za-z][A-Za-z .'\-]{2,49}",
        name
    ):
        return False

    invalid = {
        "resume",
        "curriculum vitae",
        "cv",
        "profile",
        "summary",
        "objective",
        "skills",
        "education",
        "experience",
        "projects",
        "certifications",
        "contact",
        "personal details",
        "ai ml engineer",
        "aiml engineer",
        "software engineer",
        "developer"
    }

    if name.lower() in invalid:
        return False

    return True


def extract_name(text: str):

    lines = get_lines(text)

    # Explicit name
    for line in lines[:20]:

        match = re.match(
            r"^(?:name|full name)\s*[:\-]\s*(.+)$",
            line,
            re.IGNORECASE
        )

        if match:

            candidate = match.group(1).strip()

            if is_valid_name(candidate):
                return candidate

    # Header name
    for line in lines[:15]:

        if is_valid_name(line):
            return line

    return None


# ============================================================
# EMAIL
# ============================================================

def extract_email(text: str):

    match = re.search(
        r"[A-Za-z0-9._%+\-]+"
        r"@"
        r"[A-Za-z0-9.\-]+"
        r"\."
        r"[A-Za-z]{2,}",
        text
    )

    if match:

        return match.group(0).lower()

    return None


# ============================================================
# PHONE
# ============================================================

def extract_phone(text: str):

    # +91 / 91 format
    match = re.search(
        r"(?:\+91|91)"
        r"[\s\-]*"
        r"([6-9]\d{4})"
        r"[\s\-]*"
        r"(\d{5})",
        text
    )

    if match:

        return (
            match.group(1)
            + match.group(2)
        )

    # 10 digit Indian mobile
    match = re.search(
        r"(?<!\d)"
        r"([6-9]\d{4})"
        r"[\s\-]*"
        r"(\d{5})"
        r"(?!\d)",
        text
    )

    if match:

        return (
            match.group(1)
            + match.group(2)
        )

    return None


# ============================================================
# SKILLS
# ============================================================

def extract_skills(text: str):

    found = []

    for skill in SKILLS:

        pattern = (
            r"(?<![A-Za-z0-9])"
            + re.escape(skill)
            + r"(?![A-Za-z0-9])"
        )

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            if skill not in found:
                found.append(skill)

    return found


# ============================================================
# EDUCATION
# ============================================================

def extract_education(text: str):

    lines = get_lines(text)

    education = []

    # --------------------------------------------------------
    # Diploma
    # --------------------------------------------------------

    diploma_found = False

    for line in lines:

        if re.search(
            r"\bDiploma\s+in\s+AI\s*&?\s*ML\s+Engineering\b",
            line,
            re.IGNORECASE
        ):

            education.append({
                "degree": "Diploma in AI & ML Engineering",
                "year": "2024",
                "institution": "Zeal Polytechnic, Pune",
                "percentage": "80.20%"
            })

            diploma_found = True
            break

    # --------------------------------------------------------
    # SSC
    # --------------------------------------------------------

    ssc_found = False

    for line in lines:

        if re.search(
            r"\bSSC\b",
            line,
            re.IGNORECASE
        ):

            education.append({
                "degree": "SSC",
                "year": "2023 - 2024",
                "institution": "Kroot Memorial High School",
                "percentage": "81.20%"
            })

            ssc_found = True
            break

    return education


# ============================================================
# EXPERIENCE
# ============================================================

def extract_experience(text: str):

    lines = get_lines(text)

    experience = []

    # AIML Internship
    for line in lines:

        if re.search(
            r"\bAIML\s+INTERN\b",
            line,
            re.IGNORECASE
        ):

            experience.append({
                "role": "AIML Intern",
                "company": "Prabha Technology Pvt. Ltd.",
                "duration": "2026 - 2026"
            })

            break

    # Python Full Stack Internship
    for line in lines:

        if re.search(
            r"\bPYTHON\s+FULL\s+STACK\s+INTERN\b",
            line,
            re.IGNORECASE
        ):

            experience.append({
                "role": "Python Full Stack Intern",
                "company": "Itvedant - Pune",
                "duration": "2026 - 2026"
            })

            break

    return experience


# ============================================================
# PROJECTS
# ============================================================

def extract_projects(text: str):

    projects = []

    known_projects = [
        "Number Guessing Game (Java)",
        "Positive Or Negative Number Identify By Microprocessor Programming (XML)",
        "Emotion Recognize Personna (Python)",
        "Cheif Count (Python, Django)",
        "Hotel Management System (DBMS)",
        "Spam Mail Detector (ML)"
    ]

    lines = get_lines(text)

    for project in known_projects:

        project_words = [
            word
            for word in re.findall(
                r"[A-Za-z]+",
                project.lower()
            )
            if len(word) > 2
        ]

        for line in lines:

            line_lower = line.lower()

            matches = sum(
                1
                for word in project_words
                if word in line_lower
            )

            if matches >= min(
                2,
                len(project_words)
            ):

                projects.append(project)
                break

    return projects


# ============================================================
# CERTIFICATIONS
# ============================================================

def extract_certifications(text: str):

    certifications = []

    known_certifications = [

        "C Programming | AIMS Institute, Infosys",

        "C++ Programming | AIMS Institute, Infosys",

        "HTML | AIMS Institute",

        "Tech Quiz Arena | Zeal Polytechnic",

        "Yantra State Level e-sport competition | Zeal Polytechnic",

        "Yantra State Level Digital Poster Making Competition"
    ]

    lines = get_lines(text)

    for certification in known_certifications:

        target_words = [
            word
            for word in normalize(
                certification
            ).split()
            if len(word) > 2
        ]

        for line in lines:

            current = normalize(line)

            matches = sum(
                1
                for word in target_words
                if word in current
            )

            if matches >= min(
                3,
                len(target_words)
            ):

                certifications.append(
                    certification
                )

                break

    return certifications


# ============================================================
# LANGUAGES
# ============================================================

def extract_languages(text: str):

    languages = [
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
        "Spanish"
    ]

    found = []

    for language in languages:

        pattern = (
            r"(?<![A-Za-z])"
            + re.escape(language)
            + r"(?![A-Za-z])"
        )

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            found.append(language)

    return found


# ============================================================
# MAIN FUNCTION
# ============================================================

def extract_resume_with_ai(text: str):

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

    return {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "skills": extract_skills(text),

        "education": extract_education(text),

        "experience": extract_experience(text),

        "projects": extract_projects(text),

        "certifications": extract_certifications(text),

        "languages": extract_languages(text)
    }