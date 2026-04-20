const API_URL = "http://127.0.0.1:8000";

/* =========================
   TOKEN HELPERS
========================= */
function normalizeToken(raw) {
  let token = (raw || "").trim();
  if (token.toLowerCase().startsWith("bearer ")) {
    token = token.split(" ", 2)[1] || "";
  }
  return token.replace(/^"+|"+$/g, "");
}

export function getToken() {
  return normalizeToken(localStorage.getItem("token"));
}

export function getRole() {
  return localStorage.getItem("role");
}

export function setSession(token, role) {
  localStorage.setItem("token", normalizeToken(token));
  localStorage.setItem("role", role);
}

export function clearSession() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
}

/* =========================
   SAFE FETCH
========================= */
async function safeFetch(url, options = {}) {
  const token = getToken();
  const headers = { ...(options.headers || {}) };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const res = await fetch(url, { ...options, headers });

  if (res.status === 401) {
    clearSession();
    throw new Error("Sesión expirada. Inicia sesión nuevamente.");
  }

  if (!res.ok) {
    let msg = "Error del servidor";
    try {
      msg = (await res.json()).detail || msg;
    } catch {}
    throw new Error(msg);
  }

  return res.json();
}

/* =========================
   AUTH
========================= */
export async function login(username, password) {
  const q = new URLSearchParams({ username, password }).toString();
  return safeFetch(`${API_URL}/auth/login?${q}`, { method: "POST" });
}

/* =========================
   DATA
========================= */
export const getGrades = () => safeFetch(`${API_URL}/grades/`);
export const getSubjects = () => safeFetch(`${API_URL}/subjects/`);
export const getQuarters = () => safeFetch(`${API_URL}/quarters/`);
export const getStudents = () => safeFetch(`${API_URL}/students/`);

/* =========================
   ASSESSMENTS
========================= */
export const createAssessment = (data) =>
  safeFetch(`${API_URL}/assessments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

export const excludeAssessment = (id) =>
  safeFetch(`${API_URL}/assessments/${id}/exclude`, { method: "POST" });

export const activateAssessment = (id) =>
  safeFetch(`${API_URL}/assessments/${id}/activate`, { method: "POST" });

/* =========================
   QUARTERS
========================= */
export const closeQuarter = (id) =>
  safeFetch(`${API_URL}/quarters/${id}/close`, { method: "POST" });

export const openQuarter = (id) =>
  safeFetch(`${API_URL}/quarters/${id}/open`, { method: "POST" });

/* =========================
   CALCULATION
========================= */
export const calculateQuarterGrade = (params) => {
  const q = new URLSearchParams(params).toString();
  return safeFetch(`${API_URL}/quarter-grades/calculate?${q}`, {
    method: "POST",
  });
};
