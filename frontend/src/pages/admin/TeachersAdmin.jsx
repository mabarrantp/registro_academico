import { useEffect, useState } from "react";
import "./TeachersAdmin.css";

export default function TeachersAdmin() {
    const [teachers, setTeachers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchTeachers() {
            try {
                setLoading(true);
                setError(null);

                const response = await fetch(
                    `${import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"}/teachers`,
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem("token")}`,
                        },
                    }
                );

                if (!response.ok) {
                    throw new Error("No se pudieron cargar los docentes");
                }

                const data = await response.json();
                setTeachers(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchTeachers();
    }, []);

    return (
        <div className="teachers-admin">
            <h2>Gestión de Docentes</h2>

            {loading && <p>Cargando docentes...</p>}
            {error && <p className="error">{error}</p>}

            {!loading && !error && teachers.length === 0 && (
                <p>No hay docentes registrados.</p>
            )}

            {!loading && !error && teachers.length > 0 && (
                <table className="teachers-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Apellido</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {teachers.map((t) => (
                            <tr key={t.id}>
                                <td>{t.id}</td>
                                <td>{t.first_name}</td>
                                <td>{t.last_name}</td>
                                <td>{t.email ?? "-"}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
