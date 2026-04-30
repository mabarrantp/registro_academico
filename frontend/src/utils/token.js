export function getUserFromToken() {
    const token = localStorage.getItem("token");
    if (!token) return null;

    try {
        const payload = JSON.parse(atob(token.split(".")[1]));

        // 👇 ajusta aquí si el backend usa otro campo
        const rawRole =
            payload.role ||
            payload.user_role ||
            payload.rol ||
            "";

        return {
            name: payload.name || payload.username || "Usuario",
            role: normalizeRole(rawRole),
        };
    } catch (err) {
        console.error("Token inválido", err);
        return null;
    }
}

export function getUserRole() {
    const user = getUserFromToken();
    return user?.role || null;
}

/* ✅ NORMALIZADOR DE ROL */
function normalizeRole(role) {
    const r = String(role).toLowerCase();

    if (r.includes("admin")) return "admin";
    if (r.includes("coord")) return "coordinator";
    if (r.includes("docent") || r.includes("teacher") || r.includes("guia"))
        return "teacher";

    return null;
}