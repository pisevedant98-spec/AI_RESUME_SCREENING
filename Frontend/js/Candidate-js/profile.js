document.addEventListener("DOMContentLoaded", () => {
  // Aapke existing Edit Profile button ko select karega
  const editBtn = document.querySelector(".edit-profile-btn") || document.querySelector(".profile-header-card button");
  const inputs = document.querySelectorAll(".profile-form input, .section-card input");

  if (editBtn) {
    editBtn.addEventListener("click", () => {
      // Check karo input abhi readonly/disabled hai ya nahi
      const isReadOnly = inputs[0].hasAttribute("readonly") || inputs[0].disabled;

      inputs.forEach(input => {
        if (isReadOnly) {
          input.removeAttribute("readonly");
          input.disabled = false;
          input.style.backgroundColor = "#ffffff";
          input.style.borderColor = "#00b894";
        } else {
          input.setAttribute("readonly", "true");
          input.disabled = true;
          input.style.backgroundColor = "#f8fafc";
          input.style.borderColor = "#e2e8f0";
        }
      });

      if (isReadOnly) {
        editBtn.textContent = "💾 Save Changes";
        editBtn.style.backgroundColor = "#0984e3";
      } else {
        editBtn.textContent = "✏️ Edit Profile";
        editBtn.style.backgroundColor = "#00b894";
        alert("Profile updated successfully!");
      }
    });
  }
});