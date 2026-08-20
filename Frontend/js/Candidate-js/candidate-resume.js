const resumeFile = document.getElementById("resumeFile");
const fileName = document.getElementById("fileName");

const uploadBtn = document.getElementById("uploadBtn");
const deleteBtn = document.getElementById("deleteBtn");
const downloadBtn = document.getElementById("downloadBtn");

const resumeTitle = document.getElementById("resumeTitle");
const resumeStatus = document.getElementById("resumeStatus");


/* Show selected file */

resumeFile.addEventListener("change", function () {

    if (resumeFile.files.length === 0) {
        fileName.textContent = "No file selected";
        return;
    }

    const file = resumeFile.files[0];

    fileName.textContent = file.name;
});


/* Upload */

uploadBtn.addEventListener("click", function () {

    if (resumeFile.files.length === 0) {
        alert("Please choose a resume first.");
        return;
    }

    const file = resumeFile.files[0];

    if (file.type !== "application/pdf") {
        alert("Please upload a PDF resume.");
        return;
    }

    resumeTitle.textContent = file.name;
    resumeStatus.textContent = "Resume selected successfully.";

    alert("Resume uploaded successfully.");
});


/* Delete */

deleteBtn.addEventListener("click", function () {

    resumeTitle.textContent = "No resume uploaded";
    resumeStatus.textContent = "Upload your resume to get started.";

    fileName.textContent = "No file selected";
    resumeFile.value = "";

    alert("Resume removed.");
});


/* Download */

downloadBtn.addEventListener("click", function () {

    if (resumeFile.files.length === 0) {
        alert("No resume available.");
        return;
    }

    const file = resumeFile.files[0];

    const url = URL.createObjectURL(file);

    const link = document.createElement("a");

    link.href = url;
    link.download = file.name;

    link.click();

    URL.revokeObjectURL(url);
});