document.addEventListener("DOMContentLoaded", function () {

    /* =========================
       GET ELEMENTS
       ========================= */

    const forgotPassword =
        document.getElementById("forgotPassword");

    const forgotPopup =
        document.getElementById("forgotPopup");

    const closePopup =
        document.getElementById("closePopup");

    const sendReset =
        document.getElementById("sendReset");

    const forgotEmail =
        document.getElementById("forgotEmail");

    const hrLoginForm =
        document.getElementById("hrLoginForm");


    /* =========================
       FORGOT PASSWORD
       OPEN POPUP
       ========================= */

    forgotPassword.addEventListener("click", function (event) {

        event.preventDefault();

        forgotPopup.classList.add("show");

    });


    /* =========================
       CLOSE POPUP
       ========================= */

    closePopup.addEventListener("click", function () {

        forgotPopup.classList.remove("show");

    });


    /* =========================
       SUBMIT RESET REQUEST
       ========================= */

    sendReset.addEventListener("click", function () {

        const email =
            forgotEmail.value.trim();


        if (email === "") {

            alert(
                "Please enter your registered email."
            );

            return;
        }


        alert(
            "Password reset request submitted successfully!"
        );


        forgotEmail.value = "";

        forgotPopup.classList.remove("show");

    });


    /* =========================
       CLOSE POPUP
       CLICK OUTSIDE
       ========================= */

    forgotPopup.addEventListener("click", function (event) {

        if (event.target === forgotPopup) {

            forgotPopup.classList.remove("show");

        }

    });


    /* =========================
       HR LOGIN
       ========================= */

    hrLoginForm.addEventListener("submit", function (event) {

        event.preventDefault();

        const username =
            document.getElementById("username").value.trim();

        const password =
            document.getElementById("password").value.trim();


        if (username === "" || password === "") {

            alert(
                "Please enter your username and password."
            );

            return;
        }


        /*
         * Temporary frontend login.
         *
         * Later, when backend authentication
         * is added, this section can be replaced
         * with real authentication.
         */

        window.location.href =
            "hr/hr-dashboard.html";

    });

});