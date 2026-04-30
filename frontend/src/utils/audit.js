export async function auditAction(action, module) {
    const API_URL =
        import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

    try {
        await fetch(`${API_URL}/audit/log`, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ action, module }),
        });
    } catch (err) {
        // La auditoría NO debe romper la acción principal
        console.warn("No se pudo registrar auditoría", err);
    }
}