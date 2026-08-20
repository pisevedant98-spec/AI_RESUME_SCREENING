/* =====================================================
   SKILL GAP ANALYSIS
   =====================================================

   No fake jobs.
   No fake candidates.
   No fake skills.
   No fake skill-match percentage.

   Actual data will come from backend/database.
===================================================== */

let jobs = [];
let candidates = [];
let currentAnalysis = null;


const jobSelect =
  document.getElementById("jobSelect");

const candidateSelect =
  document.getElementById("candidateSelect");

const analyzeBtn =
  document.getElementById("analyzeBtn");

const analysisContent =
  document.getElementById("analysisContent");


/* =====================================================
   LOAD JOBS
===================================================== */

async function loadJobs() {

  /*
    BACKEND CONNECTION WILL GO HERE.

    Example:

    const response =
      await fetch("/api/hr/jobs");

    jobs =
      await response.json();

    populateJobSelect();
  */

  jobSelect.innerHTML = `
    <option value="">
      No job openings available
    </option>
  `;

  candidateSelect.innerHTML = `
    <option value="">
      Select a candidate
    </option>
  `;

  candidateSelect.disabled = true;
  analyzeBtn.disabled = true;
}


/* =====================================================
   POPULATE JOB DROPDOWN
===================================================== */

function populateJobSelect() {

  if (jobs.length === 0) {

    jobSelect.innerHTML = `
      <option value="">
        No job openings available
      </option>
    `;

    return;
  }

  jobSelect.innerHTML = `
    <option value="">
      Select a job opening
    </option>
  `;

  jobs.forEach(job => {

    const option =
      document.createElement("option");

    option.value =
      job.id;

    option.textContent =
      job.title;

    jobSelect.appendChild(option);

  });
}


/* =====================================================
   JOB CHANGE
===================================================== */

jobSelect.addEventListener("change", async function () {

  const jobId =
    this.value;

  candidateSelect.innerHTML = `
    <option value="">
      Select a candidate
    </option>
  `;

  candidateSelect.disabled = true;
  analyzeBtn.disabled = true;

  resetAnalysis();

  if (!jobId) {
    return;
  }

  /*
    BACKEND CONNECTION WILL GO HERE.

    Example:

    const response =
      await fetch(
        `/api/hr/jobs/${jobId}/candidates`
      );

    candidates =
      await response.json();

    populateCandidateSelect();
  */

  candidateSelect.innerHTML = `
    <option value="">
      No candidates available
    </option>
  `;
});


/* =====================================================
   POPULATE CANDIDATES
===================================================== */

function populateCandidateSelect() {

  if (candidates.length === 0) {

    candidateSelect.innerHTML = `
      <option value="">
        No candidates available
      </option>
    `;

    candidateSelect.disabled = true;
    analyzeBtn.disabled = true;

    return;
  }

  candidateSelect.innerHTML = `
    <option value="">
      Select a candidate
    </option>
  `;

  candidates.forEach(candidate => {

    const option =
      document.createElement("option");

    option.value =
      candidate.id;

    option.textContent =
      candidate.name;

    candidateSelect.appendChild(option);

  });

  candidateSelect.disabled = false;
}


/* =====================================================
   CANDIDATE CHANGE
===================================================== */

candidateSelect.addEventListener("change", function () {

  analyzeBtn.disabled =
    !this.value;

  resetAnalysis();

});


/* =====================================================
   ANALYZE BUTTON
===================================================== */

analyzeBtn.addEventListener("click", async function () {

  const jobId =
    jobSelect.value;

  const candidateId =
    candidateSelect.value;

  if (!jobId || !candidateId) {

    alert(
      "Please select both a job and a candidate."
    );

    return;
  }

  /*
    BACKEND API WILL GO HERE.

    Example:

    const response =
      await fetch(
        "/api/hr/skill-gap-analysis",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            jobId: jobId,
            candidateId: candidateId
          })
        }
      );

    currentAnalysis =
      await response.json();

    renderAnalysis();
    updateSummary();
  */

  showBackendMessage();

});


/* =====================================================
   RENDER ANALYSIS
===================================================== */

function renderAnalysis() {

  if (!currentAnalysis) {

    resetAnalysis();

    return;
  }

  const match =
    Number(
      currentAnalysis.matchPercentage
    ) || 0;

  const matchedSkills =
    Array.isArray(
      currentAnalysis.matchedSkills
    )
      ? currentAnalysis.matchedSkills
      : [];

  const missingSkills =
    Array.isArray(
      currentAnalysis.missingSkills
    )
      ? currentAnalysis.missingSkills
      : [];


  document.getElementById(
    "matchPercentage"
  ).textContent =
    `${match}%`;


  document.getElementById(
    "matchedCount"
  ).textContent =
    matchedSkills.length;


  document.getElementById(
    "missingCount"
  ).textContent =
    missingSkills.length;


  document.getElementById(
    "analysisStatus"
  ).textContent =
    "Analysis completed";


  const matchedHtml =
    matchedSkills.length > 0

      ?

      matchedSkills.map(skill => `
        <span class="skill-tag matched-skill">
          ✓ ${escapeHtml(skill)}
        </span>
      `).join("")

      :

      `<p class="no-skills">
        No matched skills found.
      </p>`;


  const missingHtml =
    missingSkills.length > 0

      ?

      missingSkills.map(skill => `
        <span class="skill-tag missing-skill">
          ✕ ${escapeHtml(skill)}
        </span>
      `).join("")

      :

      `<p class="no-skills">
        No missing skills.
      </p>`;


  analysisContent.innerHTML = `

    <div class="match-score-box">

      <h3>
        Overall Skill Match
      </h3>

      <div class="score-number">
        ${match}%
      </div>

      <div class="score-label">
        Candidate compatibility with selected job
      </div>

      <div class="progress-container">

        <div class="progress-bar">

          <div
            class="progress-fill"
            style="width:${Math.min(match, 100)}%"
          ></div>

        </div>

      </div>

    </div>


    <div class="skills-grid">

      <div class="skills-card">

        <h3>
          ✅ Matched Skills
        </h3>

        <div class="skill-list">
          ${matchedHtml}
        </div>

      </div>


      <div class="skills-card">

        <h3>
          ❌ Missing Skills
        </h3>

        <div class="skill-list">
          ${missingHtml}
        </div>

      </div>

    </div>

  `;
}


/* =====================================================
   RESET ANALYSIS
===================================================== */

function resetAnalysis() {

  currentAnalysis = null;

  document.getElementById(
    "matchPercentage"
  ).textContent = "0%";

  document.getElementById(
    "matchedCount"
  ).textContent = "0";

  document.getElementById(
    "missingCount"
  ).textContent = "0";

  document.getElementById(
    "analysisStatus"
  ).textContent =
    "No analysis available";


  analysisContent.innerHTML = `

    <div class="empty-state">

      <div class="empty-icon">
        🧩
      </div>

      <h3>
        No Skill Gap Analysis Available
      </h3>

      <p>
        Select a job and candidate to compare the
        candidate's skills with the job requirements.
      </p>

    </div>

  `;
}


/* =====================================================
   BACKEND MESSAGE
===================================================== */

function showBackendMessage() {

  analysisContent.innerHTML = `

    <div class="empty-state">

      <div class="empty-icon">
        🔗
      </div>

      <h3>
        Backend Connection Required
      </h3>

      <p>
        The selected job and candidate are ready for
        skill-gap analysis. Once the backend and database
        are connected, the matched skills, missing skills,
        and skill-match percentage will appear here.
      </p>

    </div>

  `;


  document.getElementById(
    "analysisStatus"
  ).textContent =
    "Waiting for backend";

}


/* =====================================================
   UPDATE SUMMARY
===================================================== */

function updateSummary() {

  if (!currentAnalysis) {

    document.getElementById(
      "matchPercentage"
    ).textContent = "0%";

    document.getElementById(
      "matchedCount"
    ).textContent = "0";

    document.getElementById(
      "missingCount"
    ).textContent = "0";

    return;
  }


  document.getElementById(
    "matchPercentage"
  ).textContent =
    `${currentAnalysis.matchPercentage}%`;


  document.getElementById(
    "matchedCount"
  ).textContent =
    currentAnalysis.matchedSkills.length;


  document.getElementById(
    "missingCount"
  ).textContent =
    currentAnalysis.missingSkills.length;

}


/* =====================================================
   HTML ESCAPE
===================================================== */

function escapeHtml(value) {

  if (
    value === null ||
    value === undefined
  ) {
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
   INITIAL LOAD
===================================================== */

loadJobs();

updateSummary();