/* =====================================================
   AI SHORTLISTING
   =====================================================

   IMPORTANT:

   There are NO fake jobs.
   There are NO fake candidates.
   There are NO fake AI scores.

   Data will come from the backend/database later.

   Expected job object:

   {
     id: 1,
     title: "Software Developer",
     status: "open"
   }

   Expected candidate object:

   {
     id: 101,
     name: "Candidate Name",
     email: "candidate@email.com",
     job: "Software Developer",
     aiScore: 87,
     status: "ai-recommended",
     resumeUrl: "/uploads/resume.pdf"
   }

===================================================== */


let jobs = [];
let candidates = [];


const jobSelect =
  document.getElementById("jobSelect");

const runAiBtn =
  document.getElementById("runAiBtn");

const candidateList =
  document.getElementById("candidateList");


/* =====================================================
   LOAD JOBS
===================================================== */

async function loadJobs() {

  /*
    BACKEND CONNECTION WILL GO HERE.

    Example:

    const response = await fetch("/api/hr/jobs");
    jobs = await response.json();

    For now we intentionally do NOT add fake data.
  */

  jobSelect.innerHTML = `
    <option value="">
      No job openings available
    </option>
  `;

  updateSummary();
}


/* =====================================================
   RUN AI SHORTLISTING
===================================================== */

runAiBtn.addEventListener("click", async function () {

  const selectedJobId =
    jobSelect.value;


  if (!selectedJobId) {

    alert("Please select a job opening first.");

    return;
  }


  /*
    BACKEND API WILL GO HERE.

    Example:

    const response = await fetch(
      "/api/hr/ai-shortlisting",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          jobId: selectedJobId
        })
      }
    );

    candidates = await response.json();

    renderCandidates();
    updateSummary();
  */


  alert(
    "AI shortlisting will run here after the backend and AI service are connected."
  );

});


/* =====================================================
   RENDER CANDIDATES
===================================================== */

function renderCandidates() {

  if (candidates.length === 0) {

    candidateList.innerHTML = `

      <div class="empty-state">

        <div class="empty-icon">
          🤖
        </div>

        <h3>
          No AI Results Available
        </h3>

        <p>
          AI results will appear here when candidate
          applications and resumes are available
          and the backend completes AI analysis.
        </p>

      </div>

    `;

    document.getElementById("resultCount").textContent =
      "0 candidates";

    return;
  }


  document.getElementById("resultCount").textContent =
    `${candidates.length} candidates`;


  candidateList.innerHTML =
    candidates.map(candidate => {

      let statusText = "AI Recommended";
      let statusClass = "status-ai";


      if (candidate.status === "shortlisted") {

        statusText = "Shortlisted";
        statusClass = "status-shortlisted";

      }


      if (candidate.status === "rejected") {

        statusText = "Rejected";
        statusClass = "status-rejected";

      }


      const score =
        Number(candidate.aiScore) || 0;


      return `

        <div class="candidate-card">

          <div class="candidate-info">

            <h3>
              ${escapeHtml(candidate.name)}
            </h3>

            <p>
              📧 ${escapeHtml(candidate.email)}
            </p>

            <p>
              💼 ${escapeHtml(candidate.job)}
            </p>

            <span class="status ${statusClass}">
              ${statusText}
            </span>

          </div>


          <div class="score-box">

            <strong>
              ${score}%
            </strong>

            <span>
              AI Match Score
            </span>

            <div class="match-bar">

              <div
                class="match-fill"
                style="width:${Math.min(score, 100)}%"
              ></div>

            </div>

          </div>


          <div class="candidate-actions">

            <button
              type="button"
              class="action-btn view-btn"
              onclick="viewResume(${candidate.id})"
            >
              👁️ View Resume
            </button>


            ${
              candidate.status !== "shortlisted"
              ?
              `
                <button
                  type="button"
                  class="action-btn shortlist-btn"
                  onclick="shortlistCandidate(${candidate.id})"
                >
                  ✅ Shortlist
                </button>
              `
              :
              `
                <button
                  type="button"
                  class="action-btn reconsider-btn"
                  onclick="removeShortlist(${candidate.id})"
                >
                  ↩️ Remove Shortlist
                </button>
              `
            }


            ${
              candidate.status !== "rejected"
              ?
              `
                <button
                  type="button"
                  class="action-btn reject-btn"
                  onclick="rejectCandidate(${candidate.id})"
                >
                  ❌ Reject
                </button>
              `
              :
              `
                <button
                  type="button"
                  class="action-btn reconsider-btn"
                  onclick="reconsiderCandidate(${candidate.id})"
                >
                  🔄 Reconsider
                </button>
              `
            }

          </div>

        </div>

      `;

    }).join("");
}


/* =====================================================
   VIEW RESUME
===================================================== */

function viewResume(id) {

  const candidate =
    candidates.find(
      candidate => candidate.id === id
    );


  if (!candidate) return;


  /*
    BACKEND VERSION:

    window.open(
      candidate.resumeUrl,
      "_blank"
    );
  */


  if (candidate.resumeUrl) {

    window.open(
      candidate.resumeUrl,
      "_blank"
    );

  } else {

    alert(
      "Resume is not available."
    );

  }

}


/* =====================================================
   SHORTLIST
===================================================== */

async function shortlistCandidate(id) {

  const candidate =
    candidates.find(
      candidate => candidate.id === id
    );


  if (!candidate) return;


  /*
    BACKEND WILL LATER SAVE:

    PATCH /api/hr/candidates/:id

    {
      status: "shortlisted"
    }
  */


  candidate.status = "shortlisted";


  renderCandidates();
  updateSummary();

}


/* =====================================================
   REMOVE SHORTLIST
===================================================== */

async function removeShortlist(id) {

  const candidate =
    candidates.find(
      candidate => candidate.id === id
    );


  if (!candidate) return;


  /*
    BACKEND WILL LATER UPDATE DATABASE.
  */


  candidate.status = "ai-recommended";


  renderCandidates();
  updateSummary();

}


/* =====================================================
   REJECT
===================================================== */

async function rejectCandidate(id) {

  const candidate =
    candidates.find(
      candidate => candidate.id === id
    );


  if (!candidate) return;


  /*
    BACKEND WILL LATER SAVE:

    status = "rejected"
  */


  candidate.status = "rejected";


  renderCandidates();
  updateSummary();

}


/* =====================================================
   RECONSIDER
===================================================== */

async function reconsiderCandidate(id) {

  const candidate =
    candidates.find(
      candidate => candidate.id === id
    );


  if (!candidate) return;


  candidate.status = "ai-recommended";


  renderCandidates();
  updateSummary();

}


/* =====================================================
   SUMMARY
===================================================== */

function updateSummary() {

  const evaluated =
    candidates.length;


  const strongMatches =
    candidates.filter(
      candidate =>
        Number(candidate.aiScore) >= 80
    ).length;


  const shortlisted =
    candidates.filter(
      candidate =>
        candidate.status === "shortlisted"
    ).length;


  const rejected =
    candidates.filter(
      candidate =>
        candidate.status === "rejected"
    ).length;


  document.getElementById(
    "evaluatedCount"
  ).textContent = evaluated;


  document.getElementById(
    "strongMatchCount"
  ).textContent = strongMatches;


  document.getElementById(
    "shortlistedCount"
  ).textContent = shortlisted;


  document.getElementById(
    "rejectedCount"
  ).textContent = rejected;

}


/* =====================================================
   BASIC HTML ESCAPE
===================================================== */

function escapeHtml(value) {

  if (value === null || value === undefined) {
    return "";
  }


  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");

}


/* =====================================================
   INITIAL PAGE LOAD
===================================================== */

loadJobs();

updateSummary();

renderCandidates();