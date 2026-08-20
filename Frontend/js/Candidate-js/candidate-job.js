document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("jobSearchInput");
  const jobCards = document.querySelectorAll(".job-item-card");
  const applyButtons = document.querySelectorAll(".apply-btn");

  searchInput.addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase().trim();
    jobCards.forEach((card) => {
      const text = card.textContent.toLowerCase();
      card.style.display = text.includes(term) ? "block" : "none";
    });
  });

  applyButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const title = btn.getAttribute("data-title");
      btn.textContent = "Applied ✓";
      btn.disabled = true;
      btn.style.backgroundColor = "#94a3b8";
      btn.style.cursor = "default";
      alert(`Application submitted successfully for ${title}!`);
    });
  });
});