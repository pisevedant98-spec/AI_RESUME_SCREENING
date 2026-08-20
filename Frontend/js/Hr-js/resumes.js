/* =====================================================
   RESUME SCREENING
   =====================================================

   Backend expected candidate structure:

   {
     id: 101,
     name: "Candidate Name",
     email: "candidate@email.com",
     job: "Software Developer",
     experience: "2 Years",
     resumeUrl: "...",
     status: "pending"
   }

   No fake candidates are added here.
===================================================== */


let candidates = [];


const candidateList =
  document.getElementById("candidateList");

const searchInput =
  document.getElementById("resumeSearch");

const statusFilter =
  document.getElementById("resumeStatus");


/* =====================================================
   DISPLAY CANDIDATES
===================================================== */

function renderCandidates() {

  const searchText =
    searchInput.value
      .trim()
      .toLowerCase();

  const selectedStatus =
    statusFilter.value;


  const filteredCandidates =
    candidates.filter(function (candidate) {

      const matchesSearch =

        candidate.name
          .toLowerCase()
          .includes(searchText)

        ||

        candidate.email
          .toLowerCase()
          .includes(searchText)

        ||

        candidate.job
          .toLowerCase()
          .includes(searchText);


      const matchesStatus =

        selectedStatus === "all"

        ||

        candidate.status === selectedStatus;


      return matchesSearch && matchesStatus;

    });


  document.getElementById(
    "resumeCount"
  ).textContent =
    filteredCandidates.length + " resumes";


  /* =========================
     EMPTY STATE
  ========================= */

  if (filteredCandidates.length === 0) {

    candidateList.innerHTML = `

      <div class="empty-state">

        <div class="empty-icon">
          📄
        </div>

        <h3>
          No Resumes Available
        </h3>

        <p>
          Candidate resumes will appear here
          once applications are submitted.
        </p>

      </div>

    `;

    return;
  }


  /* =========================
     CANDIDATE CARDS
  ========================= */

  candidateList.innerHTML =

    filteredCandidates
      .map(function (candidate) {


        let statusText = "";

        let statusClass = "";


        if (candidate.status === "pending") {

          statusText =
            "Pending Review";

          statusClass =
            "status-pending";

        }


        if (candidate.status === "shortlisted") {

          statusText =
            "Shortlisted";

          statusClass =
            "status-shortlisted";

        }


        if (candidate.status === "rejected") {

          statusText =
            "Rejected";

          statusClass =
            "status-rejected";

        }


        return `

          <div class="candidate-card">


            <div class="candidate-info">

              <h3>
                ${candidate.name}
              </h3>


              <p>
                📧 ${candidate.email}
              </p>


              <p>
                💼 Applied for: ${candidate.job}
              </p>


              <p>
                🧑‍💻 Experience: ${candidate.experience}
              </p>


              <span class="status ${statusClass}">
                ${statusText}
              </span>

            </div>



            <div class="candidate-actions">


              <button
                class="action-btn view-btn"
                onclick="viewResume(${candidate.id})"
                type="button"
              >
                👁️ View Resume
              </button>


              ${
                candidate.status === "pending"

                ?

                `

                  <button
                    class="action-btn shortlist-btn"
                    onclick="shortlistCandidate(${candidate.id})"
                    type="button"
                  >
                    ✅ Shortlist
                  </button>


                  <button
                    class="action-btn reject-btn"
                    onclick="rejectCandidate(${candidate.id})"
                    type="button"
                  >
                    ❌ Reject
                  </button>

                `

                :

                ""
              }


              ${
                candidate.status === "shortlisted"

                ?

                `

                  <button
                    class="action-btn remove-btn"
                    onclick="removeShortlist(${candidate.id})"
                    type="button"
                  >
                    ↩️ Remove Shortlist
                  </button>


                  <button
                    class="action-btn reject-btn"
                    onclick="rejectCandidate(${candidate.id})"
                    type="button"
                  >
                    ❌ Reject
                  </button>

                `

                :

                ""
              }


              ${
                candidate.status === "rejected"

                ?

                `

                  <button
                    class="action-btn reconsider-btn"
                    onclick="reconsiderCandidate(${candidate.id})"
                    type="button"
                  >
                    🔄 Reconsider
                  </button>

                `

                :

                ""
              }


            </div>


          </div>

        `;

      })

      .join("");

}


/* =====================================================
   VIEW RESUME
===================================================== */

function viewResume(id) {

  const candidate =
    candidates.find(function (candidate) {

      return candidate.id === id;

    });


  if (!candidate) {
    return;
  }


  /*
    BACKEND VERSION:

    window.open(
      candidate.resumeUrl,
      "_blank"
    );

    For now there is no resume because
    backend is not connected.
  */


  alert(
    "Resume viewing will work after the backend and resume storage are connected."
  );

}


/* =====================================================
   SHORTLIST
===================================================== */

function shortlistCandidate(id) {

  const candidate =
    candidates.find(function (candidate) {

      return candidate.id === id;

    });


  if (!candidate) {
    return;
  }


  candidate.status =
    "shortlisted";


  renderCandidates();

  updateSummary();

}


/* =====================================================
   REMOVE SHORTLIST
===================================================== */

function removeShortlist(id) {

  const candidate =
    candidates.find(function (candidate) {

      return candidate.id === id;

    });


  if (!candidate) {
    return;
  }


  candidate.status =
    "pending";


  renderCandidates();

  updateSummary();

}


/* =====================================================
   REJECT
===================================================== */

function rejectCandidate(id) {

  const candidate =
    candidates.find(function (candidate) {

      return candidate.id === id;

    });


  if (!candidate) {
    return;
  }


  candidate.status =
    "rejected";


  renderCandidates();

  updateSummary();

}


/* =====================================================
   RECONSIDER
===================================================== */

function reconsiderCandidate(id) {

  const candidate =
    candidates.find(function (candidate) {

      return candidate.id === id;

    });


  if (!candidate) {
    return;
  }


  candidate.status =
    "pending";


  renderCandidates();

  updateSummary();

}


/* =====================================================
   SUMMARY
===================================================== */

function updateSummary() {

  document.getElementById(
    "totalResumes"
  ).textContent =
    candidates.length;


  document.getElementById(
    "pendingResumes"
  ).textContent =

    candidates.filter(function (candidate) {

      return candidate.status === "pending";

    }).length;


  document.getElementById(
    "shortlistedResumes"
  ).textContent =

    candidates.filter(function (candidate) {

      return candidate.status === "shortlisted";

    }).length;


  document.getElementById(
    "rejectedResumes"
  ).textContent =

    candidates.filter(function (candidate) {

      return candidate.status === "rejected";

    }).length;

}


/* =====================================================
   SEARCH
===================================================== */

searchInput.addEventListener(
  "input",
  renderCandidates
);


/* =====================================================
   FILTER
===================================================== */

statusFilter.addEventListener(
  "change",
  renderCandidates
);


/* =====================================================
   INITIAL LOAD
===================================================== */

updateSummary();

renderCandidates();