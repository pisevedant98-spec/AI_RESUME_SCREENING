document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("targetJobSelect");
  const roleTitle = document.getElementById("selectedRoleTitle");
  const matchPercent = document.getElementById("skillMatchPercent");

  if (select) {
    select.addEventListener("change", (e) => {
      const chosenText = e.target.options[e.target.selectedIndex].text;
      if (roleTitle) roleTitle.textContent = chosenText;
      if (matchPercent) matchPercent.textContent = "80%";
    });
  }
});