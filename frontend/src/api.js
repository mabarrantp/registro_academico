const API_URL = "http://127.0.0.1:8000";

// ================= TOKEN =================
function normalizeToken(raw) {
  if (typeof raw !== "string") return "";
  let token = raw.trim();
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

// ================= SAFE FETCH =================
async function safeFetch(url, options = {}) {
  const token = getToken();

  const headers = {
    ...(options.headers || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const res = await fetch(url, { ...options, headers });

  let data = null;
  try {
    data = await res.json();
  } catch {}

  if (res.status === 401) {
    clearSession();
    window.location.reload();
    throw new Error("Sesión expirada");
  }

  if (!res.ok) {
    if (Array.isArray(data?.detail)) {
      throw new Error(data.detail.map((e) => e.msg).join(", "));
    }
    if (typeof data?.detail === "string") {
      throw new Error(data.detail);
    }
    throw new Error("Error al procesar la solicitud");
  }

  return data;
}

// ================= AUTH =================
export async function login(username, password) {
  const q = new URLSearchParams({ username, password }).toString();
  return safeFetch(`${API_URL}/auth/login?${q}`, { method: "POST" });
}

// ================= DATA =================
export const getGrades = () => safeFetch(`${API_URL}/grades`);
export const getSubjects = () => safeFetch(`${API_URL}/subjects`);
export const getQuarters = () => safeFetch(`${API_URL}/quarters`);
export const getStudents = () => safeFetch(`${API_URL}/students`);

// ================= ASSESSMENTS =================

export const createAssessment = (params) => {
  const query = new URLSearchParams(params).toString();
  return safeFetch(`${API_URL}/assessments/?${query}`, {
    method: "POST",
  });
};

// ================= QUARTERS =================
export const closeQuarter = (id) =>
  safeFetch(`${API_URL}/quarters/${id}/close`, { method: "POST" });

export const openQuarter = (id) =>
  safeFetch(`${API_URL}/quarters/${id}/open`, { method: "POST" });

// ================= CALCULATION =================

export const calculateQuarterGrade = (params) => {
  const query = new URLSearchParams(params).toString();
  return safeFetch(`${API_URL}/quarter-grades/calculate?${query}`, {
    method: "POST",
  });
};
