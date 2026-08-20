/* =====================================================
   INTERVIEW MANAGEMENT
   =====================================================

   No fake candidates.
   No fake interviews.

   Data will come from the backend/database.

   Expected candidate object:

   {
     id: 101,
     name: "Candidate Name"
   }


   Expected interview object:

   {
     id: 1,
     candidateId: 101,
     candidateName: "Candidate Name",
     date: "2026-08-20",
     time: "10:30",
     type: "Technical",
     interviewer: "Interviewer Name",
     instructions: "...",
     status: "Scheduled"
   }

===================================================== */


let candidates = [];
let interviews = [];


const candidateSelect =
    document.getElementById("candidateSelect");


const interviewForm =
    document.getElementById("interviewForm");


const interviewList =
    document.getElementById("interviewList");


/* =====================================================
   LOAD CANDIDATES
===================================================== */


async function loadCandidates() {

    /*
      BACKEND API WILL GO HERE.

      Example:

      const response =
        await fetch("/api/hr/interview-candidates");

      candidates =
        await response.json();

      populateCandidates();
    */


    candidateSelect.innerHTML = `
        <option value="">
            No candidates available
        </option>
    `;
}


/* =====================================================
   POPULATE CANDIDATES
===================================================== */


function populateCandidates() {

    if (candidates.length === 0) {

        candidateSelect.innerHTML = `
            <option value="">
                No candidates available
            </option>
        `;

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
}


/* =====================================================
   SCHEDULE INTERVIEW
===================================================== */


interviewForm.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        const candidateId =
            candidateSelect.value;


        const date =
            document.getElementById(
                "interviewDate"
            ).value;


        const time =
            document.getElementById(
                "interviewTime"
            ).value;


        const type =
            document.getElementById(
                "interviewType"
            ).value;


        const interviewer =
            document.getElementById(
                "interviewer"
            ).value.trim();


        const instructions =
            document.getElementById(
                "instructions"
            ).value.trim();


        if (
            !candidateId ||
            !date ||
            !time ||
            !type ||
            !interviewer
        ) {

            alert(
                "Please fill in all required interview details."
            );

            return;
        }


        /*
          BACKEND API WILL GO HERE.

          Example:

          const response =
            await fetch(
              "/api/hr/interviews",
              {
                method: "POST",

                headers: {
                  "Content-Type": "application/json"
                },

                body: JSON.stringify({
                  candidateId,
                  date,
                  time,
                  type,
                  interviewer,
                  instructions
                })
              }
            );


          const newInterview =
            await response.json();


          interviews.push(newInterview);


          renderInterviews();
          updateSummary();
        */


        alert(
            "Interview scheduling is ready for backend connection."
        );

    }
);


/* =====================================================
   RENDER INTERVIEWS
===================================================== */


function renderInterviews() {

    if (interviews.length === 0) {

        interviewList.innerHTML = `

            <div class="empty-state">

                <div class="empty-icon">
                    📅
                </div>

                <h3>
                    No Interviews Scheduled
                </h3>

                <p>
                    Interviews will appear here after an interview
                    is scheduled for a candidate.
                </p>

            </div>

        `;


        document.getElementById(
            "interviewCount"
        ).textContent =
            "0 interviews";


        return;
    }


    document.getElementById(
        "interviewCount"
    ).textContent =
        `${interviews.length} interviews`;


    interviewList.innerHTML =
        interviews.map(interview => {

            const statusClass =
                getStatusClass(
                    interview.status
                );


            return `

                <div class="interview-card">

                    <div class="interview-info">

                        <h3>
                            ${escapeHtml(
                                interview.candidateName
                            )}
                        </h3>

                        <p>
                            📅 ${escapeHtml(
                                interview.date
                            )}
                        </p>

                        <p>
                            🕐 ${escapeHtml(
                                interview.time
                            )}
                        </p>

                        <p>
                            👤 Interviewer:
                            ${escapeHtml(
                                interview.interviewer
                            )}
                        </p>


                        <div class="interview-meta">

                            <span class="meta-tag">
                                ${escapeHtml(
                                    interview.type
                                )}
                            </span>

                        </div>


                        <span class="status ${statusClass}">
                            ${escapeHtml(
                                interview.status
                            )}
                        </span>

                    </div>


                    <div class="interview-actions">

                        ${getActionButtons(interview)}

                    </div>

                </div>

            `;

        }).join("");

}


/* =====================================================
   STATUS CLASS
===================================================== */


function getStatusClass(status) {

    switch (status) {

        case "Scheduled":
            return "status-scheduled";

        case "Completed":
            return "status-completed";

        case "Under Review":
            return "status-review";

        case "Selected":
            return "status-selected";

        case "Rejected":
            return "status-rejected";

        case "On Hold":
            return "status-hold";

        default:
            return "status-scheduled";
    }
}


/* =====================================================
   ACTION BUTTONS
===================================================== */


function getActionButtons(interview) {

    if (interview.status === "Scheduled") {

        return `

            <button
                class="action-btn complete-btn"
                onclick="updateInterviewStatus(
                    ${interview.id},
                    'Completed'
                )"
            >
                ✓ Completed
            </button>

        `;
    }


    if (interview.status === "Completed") {

        return `

            <button
                class="action-btn review-btn"
                onclick="updateInterviewStatus(
                    ${interview.id},
                    'Under Review'
                )"
            >
                🔍 Under Review
            </button>

        `;
    }


    if (interview.status === "Under Review") {

        return `

            <button
                class="action-btn select-btn"
                onclick="updateInterviewStatus(
                    ${interview.id},
                    'Selected'
                )"
            >
                ✓ Select
            </button>


            <button
                class="action-btn reject-btn"
                onclick="updateInterviewStatus(
                    ${interview.id},
                    'Rejected'
                )"
            >
                ✕ Reject
            </button>


            <button
                class="action-btn hold-btn"
                onclick="updateInterviewStatus(
                    ${interview.id},
                    'On Hold'
                )"
            >
                ⏸ On Hold
            </button>

        `;
    }


    return "";
}


/* =====================================================
   UPDATE INTERVIEW STATUS
===================================================== */


async function updateInterviewStatus(
    id,
    newStatus
) {

    const interview =
        interviews.find(
            item => item.id === id
        );


    if (!interview) {
        return;
    }


    /*
      BACKEND API WILL GO HERE.

      Example:

      await fetch(
        `/api/hr/interviews/${id}/status`,
        {
          method: "PATCH",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            status: newStatus
          })
        }
      );


      The database should store the new status.
    */


    interview.status =
        newStatus;


    renderInterviews();


    updateSummary();

}


/* =====================================================
   SUMMARY
===================================================== */


function updateSummary() {

    const scheduled =
        interviews.filter(
            interview =>
                interview.status === "Scheduled"
        ).length;


    const completed =
        interviews.filter(
            interview =>
                interview.status === "Completed"
        ).length;


    const review =
        interviews.filter(
            interview =>
                interview.status === "Under Review"
        ).length;


    const decisions =
        interviews.filter(
            interview =>
                interview.status === "Selected" ||
                interview.status === "Rejected" ||
                interview.status === "On Hold"
        ).length;


    document.getElementById(
        "scheduledCount"
    ).textContent =
        scheduled;


    document.getElementById(
        "completedCount"
    ).textContent =
        completed;


    document.getElementById(
        "reviewCount"
    ).textContent =
        review;


    document.getElementById(
        "decisionCount"
    ).textContent =
        decisions;

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


loadCandidates();


updateSummary();


renderInterviews();