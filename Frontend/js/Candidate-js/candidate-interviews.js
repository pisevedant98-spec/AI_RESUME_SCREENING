document.addEventListener("DOMContentLoaded", () => {
  const joinBtn = document.getElementById("joinMeetingBtn");
  if (joinBtn) {
    joinBtn.addEventListener("click", () => {
      alert("Redirecting to meeting room...");
    });
  }
});