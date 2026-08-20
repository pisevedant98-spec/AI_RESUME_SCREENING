document.addEventListener("DOMContentLoaded", function () {

    // Get role selection buttons
    const candidateBtn = document.getElementById("candidateBtn");
    const hrBtn = document.getElementById("hrBtn");


    // =========================
    // CANDIDATE ROLE
    // =========================

    if (candidateBtn) {
        candidateBtn.addEventListener("click", function () {

            // Go to Candidate Login
            window.location.href = "C:\Users\Admin\Desktop\Frontend\candidate-login.html";

        });
    }


    // =========================
    // HR ROLE
    // =========================

    if (hrBtn) {
        hrBtn.addEventListener("click", function () {

            // Go to HR Login
            window.location.href = "C:\\Users\\Admin\\Desktop\\Frontend\\hr-login.html";

        });
    }

});