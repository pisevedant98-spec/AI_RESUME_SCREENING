/* =====================================================
   RESUME SCREENING
   =====================================================

   Backend:
   http://127.0.0.1:8000/resume/all

===================================================== */


/* =====================================================
   GLOBAL DATA
===================================================== */

let candidates = [];


/* =====================================================
   DOM ELEMENTS
===================================================== */

const candidateList =
    document.getElementById("candidateList");

const searchInput =
    document.getElementById("resumeSearch");

const statusFilter =
    document.getElementById("resumeStatus");


/* =====================================================
   LOAD CANDIDATES FROM BACKEND
===================================================== */

async function loadCandidates() {

    try {

        console.log(
            "Loading candidates from backend..."
        );

        const result =
            await apiGet("/resume/all");


        console.log(
            "Backend candidates:",
            result
        );


        if (
            !result ||
            !Array.isArray(
                result.candidates
            )
        ) {

            console.error(
                "Invalid response from backend"
            );

            candidates = [];

            updateSummary();
            renderCandidates();

            return;
        }


        /* =============================================
           SAVE BACKEND DATA
        ============================================= */

        candidates =
            result.candidates.map(
                function (candidate) {

                    return {

                        id:
                            candidate.id ??
                            candidate.user_id,

                        user_id:
                            candidate.user_id ??
                            candidate.id,

                        name:
                            candidate.name ||
                            "Unknown Candidate",

                        email:
                            candidate.email ||
                            "No email available",

                        job:
                            candidate.job ||
                            "Candidate",

                        experience:
                            candidate.experience ||
                            "Fresher",

                        resumeUrl:
                            candidate.resumeUrl ||
                            "",

                        filename:
                            candidate.filename ||
                            "",

                        status:
                            candidate.status ||
                            "pending",

                        details:
                            candidate.details ||
                            {}
                    };

                }
            );


        console.log(
            "Candidates loaded:",
            candidates
        );


        updateSummary();

        renderCandidates();


    } catch (error) {

        console.error(
            "BACKEND CONNECTION FAILED",
            error
        );


        candidates = [];

        updateSummary();


        candidateList.innerHTML = `

            <div class="empty-state">

                <div class="empty-icon">
                    ⚠️
                </div>

                <h3>
                    Backend Connection Failed
                </h3>

                <p>
                    Please make sure the FastAPI
                    backend is running.
                </p>

            </div>

        `;

    }

}


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
        candidates.filter(
            function (candidate) {


                const name =
                    String(
                        candidate.name || ""
                    ).toLowerCase();


                const email =
                    String(
                        candidate.email || ""
                    ).toLowerCase();


                const job =
                    String(
                        candidate.job || ""
                    ).toLowerCase();


                const matchesSearch =

                    name.includes(
                        searchText
                    )

                    ||

                    email.includes(
                        searchText
                    )

                    ||

                    job.includes(
                        searchText
                    );


                const matchesStatus =

                    selectedStatus === "all"

                    ||

                    candidate.status ===
                        selectedStatus;


                return (
                    matchesSearch &&
                    matchesStatus
                );

            }
        );


    /* =============================================
       RESUME COUNT
    ============================================= */

    document.getElementById(
        "resumeCount"
    ).textContent =
        filteredCandidates.length +
        " resumes";


    /* =============================================
       EMPTY STATE
    ============================================= */

    if (
        filteredCandidates.length === 0
    ) {

        candidateList.innerHTML = `

            <div class="empty-state">

                <div class="empty-icon">
                    📄
                </div>

                <h3>
                    No Resumes Available
                </h3>

                <p>
                    Candidate resumes will appear
                    here once applications are submitted.
                </p>

            </div>

        `;

        return;
    }


    /* =============================================
       CANDIDATE CARDS
    ============================================= */

    candidateList.innerHTML =

        filteredCandidates
            .map(
                function (candidate) {


                    let statusText =
                        "Pending Review";

                    let statusClass =
                        "status-pending";


                    if (
                        candidate.status ===
                        "shortlisted"
                    ) {

                        statusText =
                            "Shortlisted";

                        statusClass =
                            "status-shortlisted";

                    }


                    if (
                        candidate.status ===
                        "rejected"
                    ) {

                        statusText =
                            "Rejected";

                        statusClass =
                            "status-rejected";

                    }


                    return `

                        <div class="candidate-card">

                            <div class="candidate-info">

                                <h3>
                                    ${escapeHtml(
                                        candidate.name
                                    )}
                                </h3>

                                <p>
                                    📧
                                    ${escapeHtml(
                                        candidate.email
                                    )}
                                </p>

                                <p>
                                    💼 Applied for:
                                    ${escapeHtml(
                                        candidate.job
                                    )}
                                </p>

                                <p>
                                    🧑‍💻 Experience:
                                    ${escapeHtml(
                                        candidate.experience
                                    )}
                                </p>

                                <span
                                    class="status ${statusClass}"
                                >
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
                                    candidate.status ===
                                    "pending"

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
                                    candidate.status ===
                                    "shortlisted"

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
                                    candidate.status ===
                                    "rejected"

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

                }
            )
            .join("");

}


/* =====================================================
   ESCAPE HTML
===================================================== */

function escapeHtml(value) {

    return String(value ?? "")
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );

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
        console.error("Candidate not found:", id);
        return;
    }

    if (!candidate.resumeUrl) {
        alert("Resume file is not available.");
        return;
    }

    console.log(
        "Opening resume:",
        candidate.resumeUrl
    );

    window.open(
        candidate.resumeUrl,
        "_blank"
    );
}


/* =====================================================
   SHORTLIST
===================================================== */

function shortlistCandidate(id) {


    const candidate =
        candidates.find(
            function (candidate) {

                return candidate.id === id;

            }
        );


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
        candidates.find(
            function (candidate) {

                return candidate.id === id;

            }
        );


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
        candidates.find(
            function (candidate) {

                return candidate.id === id;

            }
        );


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
        candidates.find(
            function (candidate) {

                return candidate.id === id;

            }
        );


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

        candidates.filter(
            function (candidate) {

                return (
                    candidate.status ===
                    "pending"
                );

            }
        ).length;


    document.getElementById(
        "shortlistedResumes"
    ).textContent =

        candidates.filter(
            function (candidate) {

                return (
                    candidate.status ===
                    "shortlisted"
                );

            }
        ).length;


    document.getElementById(
        "rejectedResumes"
    ).textContent =

        candidates.filter(
            function (candidate) {

                return (
                    candidate.status ===
                    "rejected"
                );

            }
        ).length;

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
   START APPLICATION
===================================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadCandidates();

    }
);


/* =====================================================
   LOAD RESUMES FROM BACKEND
===================================================== */

async function loadCandidates() {

    try {

        console.log("Loading resumes from backend...");

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

        console.log(
            "CANDIDATES LOADED:",
            candidates
        );

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


/* =====================================================
   INITIAL LOAD FROM BACKEND
===================================================== */

loadCandidates();