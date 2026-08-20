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

    const candidateLoginForm =
        document.getElementById("candidateLoginForm");


    /* =========================
       OPEN FORGOT PASSWORD
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
       CLOSE POPUP OUTSIDE
       ========================= */

    forgotPopup.addEventListener("click", function (event) {

        if (event.target === forgotPopup) {

            forgotPopup.classList.remove("show");

        }

    });


    /* =========================
       CANDIDATE LOGIN
       ========================= */

    candidateLoginForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();


            const email =
                document
                    .getElementById("candidate-email")
                    .value
                    .trim();


            const password =
                document
                    .getElementById("candidate-password")
                    .value
                    .trim();


            if (
                email === "" ||
                password === ""
            ) {

                alert(
                    "Please enter your email and password."
                );

                return;
            }


            /*
             * Temporary frontend login.
             *
             * Replace this with backend
             * authentication later.
             */

            window.location.href =
                "candidate/candidate-dashboard.html";

        }
    );

});