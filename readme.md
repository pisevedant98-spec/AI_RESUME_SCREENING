AI Resume Screening System

An AI-powered Resume Screening System that allows HR users to upload, process, view, and screen candidate resumes through a web-based frontend connected to a FastAPI backend.

The system extracts resume information such as:

- Candidate name
- Email
- Phone number
- Skills
- Education
- Experience
- Projects
- Certifications
- Languages

It also provides HR functionality for viewing resumes and managing candidate screening status.

---

1. Project Overview

The system consists of two main parts:

AI Resume Screening System
│
├── Frontend
│   ├── HTML
│   ├── CSS
│   └── JavaScript
│
└── Backend
    ├── FastAPI
    ├── Python
    ├── Resume Processing
    ├── AI Service
    └── Resume Storage

The frontend communicates with the FastAPI backend using HTTP APIs.

---

2. Main Features

Candidate Resume Features

- Upload PDF and DOCX resumes
- Store uploaded resumes
- Extract text from PDF resumes
- Extract candidate information
- Display candidate information
- View uploaded resumes
- Search candidates
- Filter candidates by status

HR Screening Features

Candidates can have the following statuses:

Pending
Shortlisted
Rejected

HR can:

- View resume
- Shortlist candidate
- Reject candidate
- Remove shortlist
- Reconsider rejected candidate
- Search candidates
- Filter candidates

---

3. Technologies Used

Backend

- Python
- FastAPI
- Uvicorn
- PDF processing
- DOCX support
- AI/NLP resume processing

Frontend

- HTML
- CSS
- JavaScript
- Fetch API
- Live Server

Database

The project can be connected with MySQL for storing:

- Users
- Resumes
- Candidate details
- Screening status
- Job information

---

4. Recommended Project Structure

AI Resume Screening System/
│
├── Backend/
│   │
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── routes/
│   │   │   └── resume.py
│   │   │
│   │   ├── service/
│   │   │   ├── resume_service.py
│   │   │   └── ai_service.py
│   │   │
│   │   └── utils/
│   │
│   ├── uploads/
│   │
│   ├── requirements.txt
│   └── venv/
│
└── Frontend/
    │
    ├── html/
    │
    ├── css/
    │
    └── js/
        │
        ├── api.js
        │
        └── Hr-js/
            └── resumes.js

---

5. Backend Setup

Open a terminal inside the Backend folder:

cd "D:\AI Resume Screening System\Backend"

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

If activation succeeds, the terminal should show something similar to:

(venv)

---

6. Install Dependencies

Install the required packages:

pip install fastapi uvicorn python-multipart

Install the PDF/DOCX processing libraries required by your resume service:

pip install pypdf python-docx

If the project uses additional AI/NLP libraries, install those from:

requirements.txt

using:

pip install -r requirements.txt

---

7. Start the Backend

From the Backend directory:

uvicorn app.main:app --reload

Successful startup should look similar to:

INFO:     Uvicorn running on http://127.0.0.1:8000

The backend API is now available at:

http://127.0.0.1:8000

---

8. FastAPI Documentation

FastAPI automatically provides Swagger documentation.

Open:

http://127.0.0.1:8000/docs

This is useful for testing APIs before connecting the frontend.

---

9. Backend API Endpoints

Upload Resume

POST /resume/upload

Parameters:

user_id
file

Example:

POST http://127.0.0.1:8000/resume/upload?user_id=11

The uploaded file is stored inside:

Backend/uploads/

Example filename:

user_11_resume chinmayee.pdf

---

10. Extract Resume Text

GET /resume/extract/{user_id}

Example:

GET http://127.0.0.1:8000/resume/extract/11

Example response:

{
    "user_id": 11,
    "filename": "user_11_resume chinmayee.pdf",
    "text": "CHINMAYEE PARAB..."
}

This endpoint returns the raw extracted resume text.

---

11. Extract Candidate Details

GET /resume/details/{user_id}

Example:

GET http://127.0.0.1:8000/resume/details/11

Example response:

{
    "user_id": 11,
    "filename": "user_11_resume chinmayee.pdf",
    "details": {
        "name": "CHINMAYEE PARAB",
        "email": "chinmayee.parab289@gmail.com",
        "phone": "8446694090",
        "skills": [],
        "education": [],
        "experience": [],
        "projects": [],
        "certifications": [],
        "languages": []
    }
}

The actual returned information depends on the resume processing logic.

---

12. Get All Resumes

GET /resume/all

Example:

http://127.0.0.1:8000/resume/all

This endpoint is used by the HR frontend.

Example structure:

{
    "count": 1,
    "candidates": [
        {
            "id": 11,
            "user_id": 11,
            "name": "CHINMAYEE PARAB",
            "email": "chinmayee.parab289@gmail.com",
            "job": "Computer Engineering",
            "experience": "Cloud Computing Intern - Jalgi Technologies Pvt. Ltd.",
            "resumeUrl": "http://127.0.0.1:8000/resume/file/11",
            "filename": "user_11_resume chinmayee.pdf",
            "status": "pending",
            "details": {}
        }
    ]
}

---

13. View Resume PDF

GET /resume/file/{user_id}

Example:

http://127.0.0.1:8000/resume/file/11

The endpoint should return the PDF with:

Content-Disposition: inline

so supported browsers can display the PDF directly instead of forcing a download.

Recommended implementation:

@router.get("/file/{user_id}")
def view_resume(user_id: int):

    file_path = None

    for filename in os.listdir(UPLOAD_DIR):

        if (
            filename.startswith(f"user_{user_id}_")
            and filename.lower().endswith(".pdf")
        ):
            file_path = os.path.join(
                UPLOAD_DIR,
                filename
            )
            break

    if not file_path:
        raise HTTPException(
            status_code=404,
            detail="Resume PDF not found"
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "inline"
        }
    )

---

14. Frontend API Configuration

The frontend uses:

Frontend/js/api.js

The API base URL is:

const API_BASE_URL = "http://127.0.0.1:8000";

The frontend communicates with FastAPI through the Fetch API.

---

15. Frontend API Functions

The "api.js" file provides reusable functions:

apiRequest()
apiJson()
apiGet()
apiPost()
apiUpload()
apiPatch()
apiDelete()

For example:

const result =
    await apiGet("/resume/all");

This sends:

GET http://127.0.0.1:8000/resume/all

---

16. Frontend Resume Page

The HR resume page uses:

Frontend/js/Hr-js/resumes.js

This file is responsible for:

- Loading candidates
- Displaying candidates
- Searching candidates
- Filtering candidates
- Viewing resumes
- Shortlisting candidates
- Rejecting candidates
- Reconsidering candidates
- Updating resume counters

---

17. Loading Candidates From Backend

The frontend should load candidates using:

async function loadCandidates() {

    try {

        console.log(
            "Loading resumes from backend..."
        );

        const result =
            await apiGet("/resume/all");

        console.log(
            "BACKEND RESPONSE:",
            result
        );

        if (
            result &&
            Array.isArray(result.candidates)
        ) {

            candidates =
                result.candidates;

        } else {

            candidates = [];

        }

        updateSummary();

        renderCandidates();

    } catch (error) {

        console.error(
            "FAILED TO LOAD RESUMES:",
            error
        );

        candidates = [];

        updateSummary();

        renderCandidates();

        alert(
            "Could not connect to the backend. Make sure FastAPI is running."
        );
    }
}

loadCandidates();

---

18. View Resume From Frontend

The frontend receives the resume URL from:

/resume/all

Example:

"resumeUrl": "http://127.0.0.1:8000/resume/file/11"

The "viewResume()" function should open that URL:

function viewResume(id) {

    const candidate =
        candidates.find(function (candidate) {
            return candidate.id === id;
        });

    if (!candidate) {
        console.error(
            "Candidate not found:",
            id
        );
        return;
    }

    if (!candidate.resumeUrl) {
        alert(
            "Resume file is not available."
        );
        return;
    }

    window.open(
        candidate.resumeUrl,
        "_blank"
    );
}

---

19. Frontend HTML Script Order

The HTML page must load "api.js" before "resumes.js".

Use:

<script src="../js/api.js"></script>
<script src="../js/Hr-js/resumes.js"></script>

The order is important because "resumes.js" uses functions such as:

apiGet()

which are defined in:

api.js

---

20. Frontend → Backend Connection

The complete connection works like this:

HR opens Resume Page
        ↓
resumes.js loads
        ↓
loadCandidates()
        ↓
apiGet("/resume/all")
        ↓
api.js
        ↓
FastAPI
        ↓
GET /resume/all
        ↓
Backend scans uploads/
        ↓
Resume text extraction
        ↓
Candidate detail extraction
        ↓
JSON response
        ↓
Frontend receives candidates
        ↓
renderCandidates()
        ↓
Candidate cards displayed

---

21. Resume Viewing Flow

When HR clicks:

👁️ View Resume

the flow is:

View Resume button
        ↓
viewResume(id)
        ↓
candidate.resumeUrl
        ↓
window.open()
        ↓
GET /resume/file/{user_id}
        ↓
FastAPI
        ↓
FileResponse
        ↓
PDF displayed in browser

---

22. Testing the Connection

Before testing the frontend, make sure FastAPI is running:

uvicorn app.main:app --reload

Then test:

http://127.0.0.1:8000/docs

If Swagger opens, FastAPI is running.

Next test:

http://127.0.0.1:8000/resume/all

If JSON containing candidates appears, the backend resume API is working.

Then open the frontend using Live Server.

Open the browser developer console:

F12 → Console

You should see:

Loading resumes from backend...
BACKEND RESPONSE:
CANDIDATES LOADED:

---

23. Testing Resume Viewing

For user ID "11", test:

http://127.0.0.1:8000/resume/file/11

If the PDF opens in the browser, resume file serving is working.

Then return to the HR page and click:

👁️ View Resume

The same PDF should open in a new browser tab.

---

24. Common Errors

Error: Failed to fetch

Possible causes:

- FastAPI is not running
- Wrong API URL
- CORS is not configured
- Incorrect frontend endpoint

Check:

const API_BASE_URL =
    "http://127.0.0.1:8000";

and make sure FastAPI is running.F

---

25. CORS Configuration

If the frontend is running from a different origin, configure CORS in "app/main.py".

Example:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

For development, "["*"]" is convenient.

For production, replace it with the actual frontend origin.

---

26. Error: 404 Resume Not Found

If:

GET /resume/file/11

returns:

404 Resume file not found

check:

Backend/uploads/

and verify that the file exists with a name beginning with:

user_11_

Example:

user_11_resume chinmayee.pdf

---

27. Error: ImportError

Example:

ImportError:
cannot import name 'extract_text_from_pdf'

Check:

Backend/app/service/resume_service.py

and make sure the required function exists:

def extract_text_from_pdf(...):
    ...

Likewise, if "resume.py" imports:

extract_candidate_details

that function must exist in:

app/service/resume_service.py

---

28. Important Backend Rule

Do not create multiple copies of the same router code in "resume.py".

There should be one:

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

and one implementation of each endpoint.

Avoid duplicate imports and duplicate route definitions.

---

29. Important Frontend Rule

Do not create multiple copies of:

loadCandidates();

Keep one initial backend load.

Also make sure:

<script src="../js/api.js"></script>

comes before:

<script src="../js/Hr-js/resumes.js"></script>

---

30. Current System Flow

The current system can be understood as:

                    AI RESUME SCREENING SYSTEM
                              │
             ┌────────────────┴────────────────┐
             │                                 │
          FRONTEND                          BACKEND
             │                                 │
       HTML / CSS / JS                      FastAPI
             │                                 │
        api.js                              routes/
             │                                 │
      resumes.js                       resume.py
             │                                 │
             └──────────── HTTP ───────────────┘
                              │
                         Resume Service
                              │
                         AI Service
                              │
                       Resume Processing
                              │
                         uploads/
                              │
                           PDF/DOCX

---

31. Recommended Development Order

Build and test the system in this order:

1. Start FastAPI
        ↓
2. Test /docs
        ↓
3. Test resume upload
        ↓
4. Test /resume/extract/{user_id}
        ↓
5. Test /resume/details/{user_id}
        ↓
6. Test /resume/all
        ↓
7. Connect frontend api.js
        ↓
8. Load candidates in resumes.js
        ↓
9. Display candidate cards
        ↓
10. Connect View Resume
        ↓
11. Connect Shortlist
        ↓
12. Connect Reject
        ↓
13. Connect candidate details
        ↓
14. Connect MySQL
        ↓
15. Add AI job matching/scoring

---

32. Future AI Screening Features

After the basic frontend/backend connection is stable, the AI screening system can be extended with:

- Resume-to-job matching
- Skill matching
- Candidate scoring
- Missing skill detection
- Experience matching
- Education matching
- Job recommendation
- Resume ranking
- Candidate ranking
- AI-generated screening summary
- Interview recommendation

Example:

Candidate Resume
       ↓
Resume Parser
       ↓
Candidate Profile
       ↓
Job Description
       ↓
AI Matching
       ↓
Match Score
       ↓
HR Dashboard

---

33. Example Candidate Screening Result

A future screening response could look like:

{
    "candidate_id": 11,
    "job": "Python Developer",
    "match_score": 87,
    "matched_skills": [
        "Python",
        "Django",
        "HTML",
        "CSS",
        "MongoDB"
    ],
    "missing_skills": [
        "Docker"
    ],
    "recommendation": "Shortlist"
}

---

34. Development Checklist

Backend

- [ ] FastAPI installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] "app/main.py" working
- [ ] "resume.py" working
- [ ] "resume_service.py" working
- [ ] "ai_service.py" working
- [ ] "uploads/" directory created
- [ ] "/docs" working
- [ ] "/resume/upload" working
- [ ] "/resume/extract/{user_id}" working
- [ ] "/resume/details/{user_id}" working
- [ ] "/resume/all" working
- [ ] "/resume/file/{user_id}" working

Frontend

- [ ] "api.js" created
- [ ] Correct backend URL configured
- [ ] "resumes.js" loaded
- [ ] "api.js" loaded before "resumes.js"
- [ ] Candidates loaded from backend
- [ ] Candidate cards displayed
- [ ] Search working
- [ ] Status filter working
- [ ] View Resume working

Database

- [ ] MySQL installed
- [ ] Database created
- [ ] Tables created
- [ ] Backend database connection configured
- [ ] Candidate records connected to resumes

---

35. How to Run the Project

Terminal 1 — Backend

cd "D:\AI Resume Screening System\Backend"

Activate environment:

venv\Scripts\activate

Run FastAPI:

uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

---

Terminal 2 — Frontend

Open the Frontend folder in VS Code.

Use the VS Code Live Server extension.

Open the required HTML page using:

Open with Live Server

The frontend will communicate with:

http://127.0.0.1:8000

---

36. Final Architecture

                     ┌─────────────────────┐
                     │      HR USER        │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │      FRONTEND       │
                     │                     │
                     │ HTML / CSS / JS     │
                     │ api.js              │
                     │ resumes.js          │
                     └──────────┬──────────┘
                                │
                         HTTP / REST API
                                │
                                ▼
                     ┌─────────────────────┐
                     │       FASTAPI       │
                     │                     │
                     │ resume.py           │
                     │ routes              │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │  RESUME SERVICE     │
                     │                     │
                     │ PDF extraction      │
                     │ Resume processing   │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │     AI SERVICE      │
                     │                     │
                     │ Information         │
                     │ extraction          │
                     │ Skill detection     │
                     │ Resume analysis     │
                     └──────────┬──────────┘
                                │
                       ┌────────┴────────┐
                       │                 │
                       ▼                 ▼
                ┌─────────────┐   ┌─────────────┐
                │   MySQL     │   │   uploads/  │
                │  Database   │   │ PDF / DOCX  │
                └─────────────┘   └─────────────┘

---

37. Project Status

The basic frontend-backend resume connection consists of:

✅ FastAPI backend
✅ Resume upload
✅ Resume storage
✅ PDF text extraction
✅ Candidate detail extraction
✅ Get all resumes API
✅ Frontend API configuration
✅ Frontend candidate loading
✅ Candidate cards
✅ Resume search
✅ Resume status filter
✅ Resume PDF endpoint
✅ Browser PDF viewing

The next major development stage is:

Database integration
        ↓
Persistent candidate status
        ↓
Candidate details UI
        ↓
Job description input
        ↓
AI resume-job matching
        ↓
Candidate scoring
        ↓
Automatic ranking
        ↓
HR screening dashboard

---

38. Important Note

This project is currently designed for local development.

The default backend address is:

http://127.0.0.1:8000

Before deployment, update:

- API URL
- CORS configuration
- Database credentials
- File storage
- Authentication
- Authorization
- Security settings
- Production server configuration

Never commit real passwords, API keys, or database credentials to GitHub.

---

39. Quick Start

For a quick start:

cd "D:\AI Resume Screening System\Backend"
venv\Scripts\activate
uvicorn app.main:app --reload

Then open:

http://127.0.0.1:8000/docs

Test:

GET /resume/all

Then open the frontend using VS Code Live Server.

The frontend should automatically request:

GET /resume/all

and display the resumes stored by the backend.

---

End

AI Resume Screening System

Frontend + FastAPI Backend + Resume Processing + AI Screening + MySQL

Upload → Extract → Analyze → Display → Screen → Rank