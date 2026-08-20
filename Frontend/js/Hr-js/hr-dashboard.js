document.addEventListener("DOMContentLoaded", () => {
  const stats = {
    activeJobs: document.getElementById("activeJobs"),
    totalApplications: document.getElementById("totalApplications"),
    shortlisted: document.getElementById("shortlisted"),
    interviews: document.getElementById("interviews")
  };

  const jobsContainer = document.getElementById("recentJobs");
  const applicationsContainer = document.getElementById("recentApplications");
  const interviewsContainer = document.getElementById("upcomingInterviews");

  function getData(key, fallback = []) {
    try {
      const data = JSON.parse(localStorage.getItem(key));
      return Array.isArray(data) ? data : fallback;
    } catch (error) {
      console.error(`Error reading ${key}:`, error);
      return fallback;
    }
  }

  function updateStats() {
    const jobs = getData("jobs");
    const applications = getData("applications");
    const interviewsData = getData("interviews");

    const shortlistedData = applications.filter(
      application =>
        application.status &&
        application.status.toLowerCase() === "shortlisted"
    );

    stats.activeJobs.textContent = jobs.length;
    stats.totalApplications.textContent = applications.length;
    stats.shortlisted.textContent = shortlistedData.length;
    stats.interviews.textContent = interviewsData.length;
  }

  function showEmpty(container, icon, title, text) {
    if (!container) return;

    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">${icon}</div>
        <h3>${title}</h3>
        <p>${text}</p>
      </div>
    `;
  }

  function renderJobs() {
    const jobs = getData("jobs");

    if (!jobsContainer) return;

    if (jobs.length === 0) {
      showEmpty(
        jobsContainer,
        "💼",
        "No Job Openings",
        "Job openings created through Job Management will appear here."
      );
      return;
    }

    jobsContainer.innerHTML = jobs
      .slice(0, 5)
      .map(job => {
        const title = job.title || job.jobTitle || "Untitled Position";
        const location = job.location || "Location not specified";

        return `
          <div class="recent-item">
            <div class="recent-item-icon">💼</div>

            <div class="recent-item-info">
              <h3>${title}</h3>
              <p>${location}</p>
            </div>

            <span class="status-badge">
              ${job.status || "Open"}
            </span>
          </div>
        `;
      })
      .join("");
  }

  function renderApplications() {
    const applications = getData("applications");

    if (!applicationsContainer) return;

    if (applications.length === 0) {
      showEmpty(
        applicationsContainer,
        "👥",
        "No Applications",
        "Candidate applications will appear here when they are available."
      );
      return;
    }

    applicationsContainer.innerHTML = applications
      .slice(0, 5)
      .map(application => {
        const name =
          application.candidateName ||
          application.name ||
          "Unknown Candidate";

        const job =
          application.jobTitle ||
          application.position ||
          "Job not specified";

        const status = application.status || "Pending";

        return `
          <div class="recent-item">
            <div class="recent-item-icon">👤</div>

            <div class="recent-item-info">
              <h3>${name}</h3>
              <p>${job}</p>
            </div>

            <span class="status-badge">
              ${status}
            </span>
          </div>
        `;
      })
      .join("");
  }

  function renderInterviews() {
    const interviewsData = getData("interviews");

    if (!interviewsContainer) return;

    if (interviewsData.length === 0) {
      showEmpty(
        interviewsContainer,
        "📅",
        "No Upcoming Interviews",
        "Scheduled interviews will appear here."
      );
      return;
    }

    interviewsContainer.innerHTML = interviewsData
      .slice(0, 5)
      .map(interview => {
        const candidate =
          interview.candidateName ||
          interview.candidate ||
          "Candidate";

        const date =
          interview.date ||
          interview.interviewDate ||
          "Date not specified";

        const time =
          interview.time ||
          interview.interviewTime ||
          "";

        return `
          <div class="recent-item">
            <div class="recent-item-icon">📅</div>

            <div class="recent-item-info">
              <h3>${candidate}</h3>
              <p>${date}${time ? ` • ${time}` : ""}</p>
            </div>
          </div>
        `;
      })
      .join("");
  }

  function initDashboard() {
    updateStats();
    renderJobs();
    renderApplications();
    renderInterviews();
  }

  initDashboard();

  // Refresh dashboard when another page changes localStorage
  window.addEventListener("storage", initDashboard);
});