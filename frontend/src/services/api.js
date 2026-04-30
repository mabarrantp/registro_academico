/**
 * API Service
 * Comunicación centralizada con el backend
 * Modo PRODUCTION-READY
 */

// 🔁 En producción real, usar variable de entorno
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

/**
 * Obtener token JWT
 */
function getAuthToken() {
    return localStorage.getItem("token");
}

/**
 * Headers base
 */
function getHeaders(isJson = true) {
    const headers = {};

    const token = getAuthToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    if (isJson) {
        headers["Content-Type"] = "application/json";
    }

    return headers;
}

/**
 * Manejo estándar de respuestas HTTP
 */
async function handleResponse(response) {
    if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        const message =
            data.detail ||
            data.message ||
            "Error al comunicarse con el servidor";
        throw new Error(message);
    }
    return response;
}

//
// =====================================================
// AUTH
// =====================================================
//

export async function login(credentials) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify(credentials),
    });

    await handleResponse(response);
    return response.json();
}

//
// =====================================================
// GRADES
// =====================================================
//

export async function getGrades({ studentId, sectionId, quarterId } = {}) {
    const params = new URLSearchParams();

    if (studentId) params.append("student_id", studentId);
    if (sectionId) params.append("section_id", sectionId);
    if (quarterId) params.append("quarter_id", quarterId);

    const response = await fetch(
        `${API_BASE_URL}/grades?${params.toString()}`,
        { headers: getHeaders(false) }
    );

    await handleResponse(response);
    return response.json();
}

export async function getFinalAverage(studentId) {
    const response = await fetch(
        `${API_BASE_URL}/grades/final-average?student_id=${studentId}`,
        { headers: getHeaders(false) }
    );

    await handleResponse(response);
    return response.json();
}

//
// =====================================================
// REPORT CARD
// =====================================================
//

export async function getReportCard(studentId, academicYear) {
    const response = await fetch(
        `${API_BASE_URL}/report-card?student_id=${studentId}&academic_year=${academicYear}`,
        { headers: getHeaders(false) }
    );

    await handleResponse(response);
    return response.json();
}

export async function downloadReportCardPDF(studentId, academicYear) {
    const response = await fetch(
        `${API_BASE_URL}/report-card/pdf?student_id=${studentId}&academic_year=${academicYear}`,
        { headers: getHeaders(false) }
    );

    if (!response.ok) {
        throw new Error("No se pudo descargar el PDF");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    window.open(url);
}

//
// =====================================================
// CATALOGOS (selección dinámica)
// =====================================================
//

export async function getStudents() {
    const response = await fetch(`${API_BASE_URL}/students`, {
        headers: getHeaders(false),
    });

    await handleResponse(response);
    return response.json();
}

export async function getSections() {
    const response = await fetch(`${API_BASE_URL}/sections`, {
        headers: getHeaders(false),
    });

    await handleResponse(response);
    return response.json();
}

export async function getAcademicYears() {
    const response = await fetch(`${API_BASE_URL}/academic-years`, {
        headers: getHeaders(false),
    });

    await handleResponse(response);
    return response.json();
}