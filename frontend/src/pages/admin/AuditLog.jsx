import { useEffect, useState } from "react";

export default function AuditLog() {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const API_URL =
        import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

    useEffect(() => {
        async function loadLogs() {
            try {
                const response = await fetch(`${API_URL}/audit/logs`, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    },
                });

                if (!response.ok) {
                    throw new Error("Error al obtener auditoría");
                }

                const data = await response.json();
                setLogs(data);
            } catch (err) {
                console.error(err);
                setError("No se pudo cargar la auditoría");
            } finally {
                setLoading(false);
            }
        }

        loadLogs();
    }, []);

    if (loading) {
        return <p>Cargando auditoría…</p>;
    }

    if (error) {
        return <p style={{ color: "red" }}>{error}</p>;
    }

    return (
        <div>
            <h2>Auditoría del Sistema</h2>

            {logs.length === 0 ? (
                <p>No hay acciones registradas.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Usuario</th>
                            <th>Rol</th>
                            <th>Acción</th>
                            <th>Módulo</th>
                            <th>Fecha</th>
                        </tr>
                    </thead>
                    <tbody>
                        {logs.map((log) => (
                            <tr key={log.id}>
                                <td>{log.user}</td>
                                <td>{log.role}</td>
                                <td>{log.action}</td>
                                <td>{log.module}</td>
                                <td>
                                    {new Date(log.timestamp).toLocaleString()}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
