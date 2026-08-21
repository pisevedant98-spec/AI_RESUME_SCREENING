// ============================================================
// AI RESUME SCREENING SYSTEM
// FRONTEND API CONFIGURATION
// ============================================================

const API_BASE_URL = "http://127.0.0.1:8000";


// ============================================================
// GENERIC API REQUEST
// ============================================================

async function apiRequest(endpoint, options = {}) {

    const url = `${API_BASE_URL}${endpoint}`;

    const response = await fetch(url, options);

    if (!response.ok) {

        let message = `Request failed: ${response.status}`;

        try {

            const errorData = await response.json();

            if (errorData.detail) {
                message = errorData.detail;
            }

        } catch (error) {
            // Ignore JSON parsing error
        }

        throw new Error(message);
    }

    return response;
}


// ============================================================
// JSON REQUEST
// ============================================================

async function apiJson(endpoint, options = {}) {

    const response = await apiRequest(endpoint, options);

    return await response.json();
}


// ============================================================
// GET
// ============================================================

async function apiGet(endpoint) {

    return await apiJson(endpoint, {
        method: "GET"
    });
}


// ============================================================
// POST JSON
// ============================================================

async function apiPost(endpoint, data) {

    return await apiJson(endpoint, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });
}


// ============================================================
// POST FILE
// ============================================================

async function apiUpload(endpoint, file, additionalData = {}) {

    const formData = new FormData();

    formData.append("file", file);


    Object.keys(additionalData).forEach(function (key) {

        formData.append(
            key,
            additionalData[key]
        );

    });


    return await apiJson(endpoint, {

        method: "POST",

        body: formData

    });
}


// ============================================================
// PATCH JSON
// ============================================================

async function apiPatch(endpoint, data) {

    return await apiJson(endpoint, {

        method: "PATCH",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(data)

    });
}


// ============================================================
// DELETE
// ============================================================

async function apiDelete(endpoint) {

    const response =
        await apiRequest(endpoint, {
            method: "DELETE"
        });

    return await response.json();

}