document.addEventListener("DOMContentLoaded", () => {
  const markReadBtn = document.getElementById("markAllReadBtn");
  const unreadCards = document.querySelectorAll(".notification-card.unread");

  if (markReadBtn) {
    markReadBtn.addEventListener("click", () => {
      unreadCards.forEach(card => {
        card.classList.remove("unread");
      });
      alert("All notifications marked as read.");
    });
  }
});