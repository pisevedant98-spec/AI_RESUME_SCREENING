/* =====================================================
   JOB MANAGEMENT (Synced with localStorage)
   ===================================================== */

let jobs = JSON.parse(localStorage.getItem("company_jobs")) || [];

const jobModal = document.getElementById("jobModal");
const createJobBtn = document.getElementById("createJobBtn");
const emptyCreateBtn = document.getElementById("emptyCreateBtn");
const closeJobModal = document.getElementById("closeJobModal");
const cancelJob = document.getElementById("cancelJob");
const createJobForm = document.getElementById("createJobForm");

const jobList = document.getElementById("jobList");
const jobSearch = document.getElementById("jobSearch");
const jobStatus = document.getElementById("jobStatus");

const jobCount = document.getElementById("jobCount");

const activeJobCount = document.getElementById("activeJobCount");
const closedJobCount = document.getElementById("closedJobCount");
const totalJobCount = document.getElementById("totalJobCount");

function saveJobsToStorage() {
  localStorage.setItem("company_jobs", JSON.stringify(jobs));
}

/* =====================================================
   MODAL CONTROLS
   ===================================================== */
function openJobModal() {
  if (jobModal) jobModal.classList.add("show");
}

function closeModal() {
  if (jobModal) jobModal.classList.remove("show");
}

if (createJobBtn) createJobBtn.addEventListener("click", openJobModal);
if (emptyCreateBtn) emptyCreateBtn.addEventListener("click", openJobModal);
if (closeJobModal) closeJobModal.addEventListener("click", closeModal);
if (cancelJob) cancelJob.addEventListener("click", closeModal);

if (jobModal) {
  jobModal.addEventListener("click", function (event) {
    if (event.target === jobModal) closeModal();
  });
}

/* =====================================================
   CREATE JOB
   ===================================================== */
if (createJobForm) {
  createJobForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const title = document.getElementById("jobTitle").value.trim();
    const location = document.getElementById("jobLocation").value.trim();
    const description = document.getElementById("jobDescription").value.trim();
    const skills = document.getElementById("jobSkills").value.trim();
    const experience = document.getElementById("jobExperience").value;
    const education = document.getElementById("jobEducation").value.trim();
    const type = document.getElementById("jobType").value;
    const salary = document.getElementById("jobSalary").value.trim();

    if (!title || !location || !description || !skills || !experience || !education || !type || !salary) {
      alert("Please fill all job details.");
      return;
    }

    const newJob = {
      id: Date.now(),
      title: title,
      location: location,
      description: description,
      skills: skills,
      experience: experience,
      education: education,
      type: type,
      salary: salary,
      status: "open",
      createdAt: new Date().toLocaleDateString()
    };

    jobs.push(newJob);
    saveJobsToStorage();

    createJobForm.reset();
    closeModal();
    renderJobs();
    updateCounters();
  });
}

/* =====================================================
   CLOSE & REOPEN JOB
   ===================================================== */
function closeJob(id) {
  const job = jobs.find(item => item.id === id);
  if (!job) return;
  if (!confirm("Are you sure you want to close this job?")) return;

  job.status = "closed";
  saveJobsToStorage();
  renderJobs();
  updateCounters();
}

function reopenJob(id) {
  const job = jobs.find(item => item.id === id);
  if (!job) return;

  job.status = "open";
  saveJobsToStorage();
  renderJobs();
  updateCounters();
}

/* =====================================================
   SEARCH & FILTER
   ===================================================== */
function getFilteredJobs() {
  const searchValue = jobSearch ? jobSearch.value.trim().toLowerCase() : "";
  const selectedStatus = jobStatus ? jobStatus.value : "all";

  return jobs.filter(function (job) {
    const matchesSearch =
      job.title.toLowerCase().includes(searchValue) ||
      job.location.toLowerCase().includes(searchValue) ||
      job.skills.toLowerCase().includes(searchValue);

    const matchesStatus =
      selectedStatus === "all" || job.status === selectedStatus;

    return matchesSearch && matchesStatus;
  });
}

if (jobSearch) jobSearch.addEventListener("input", renderJobs);
if (jobStatus) jobStatus.addEventListener("change", renderJobs);

function escapeHTML(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/* =====================================================
   RENDER JOBS (HR)
   ===================================================== */
function renderJobs() {
  if (!jobList) return;
  const filteredJobs = getFilteredJobs();

  if (filteredJobs.length === 0) {
    jobList.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">💼</div>
        <h3>No Job Openings Yet</h3>
        <p>Create your first job opening to start receiving candidates.</p>
        <button class="primary-btn" type="button" onclick="openJobModal()">+ Create New Job</button>
      </div>
    `;
    updateJobCount(0);
    return;
  }

  jobList.innerHTML = filteredJobs.map(function (job) {
    const statusText = job.status === "open" ? "Open" : "Closed";
    const actionButton = job.status === "open"
      ? `<button class="close-job-btn" type="button" onclick="closeJob(${job.id})">Close Job</button>`
      : `<button class="reopen-job-btn" type="button" onclick="reopenJob(${job.id})">Reopen Job</button>`;

    return `
      <article class="job-card">
        <span class="job-status ${job.status}">${statusText}</span>
        <h3>${escapeHTML(job.title)}</h3>
        <p>📍 <strong>Location:</strong> ${escapeHTML(job.location)}</p>
        <p>💼 <strong>Employment:</strong> ${escapeHTML(job.type)}</p>
        <p>🎓 <strong>Education:</strong> ${escapeHTML(job.education)}</p>
        <p>🧑‍💻 <strong>Experience:</strong> ${escapeHTML(job.experience)}</p>
        <p>💰 <strong>Salary:</strong> ${escapeHTML(job.salary)}</p>
        <p>🛠️ <strong>Skills:</strong> ${escapeHTML(job.skills)}</p>
        <p>📝 <strong>Description:</strong> ${escapeHTML(job.description)}</p>
        <p>📅 <strong>Created:</strong> ${escapeHTML(job.createdAt)}</p>
        <div class="job-actions">
          ${actionButton}
        </div>
      </article>
    `;
  }).join("");

  updateJobCount(filteredJobs.length);
}

function updateJobCount(count) {
  if (!jobCount) return;
  jobCount.textContent = count === 0 ? "No jobs available" : (count === 1 ? "1 job" : `${count} jobs`);
}

function updateCounters() {
  if (!activeJobCount || !closedJobCount || !totalJobCount) return;
  const activeJobs = jobs.filter(j => j.status === "open").length;
  const closedJobs = jobs.filter(j => j.status === "closed").length;

  activeJobCount.textContent = activeJobs;
  closedJobCount.textContent = closedJobs;
  totalJobCount.textContent = jobs.length;
}

renderJobs();
updateCounters();