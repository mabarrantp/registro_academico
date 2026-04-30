import { useEffect, useState } from "react";
import "./SubjectsAdmin.css";

export default function SubjectsAdmin() {
    const [subjects, setSubjects] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchSubjects() {
            try {
                setLoading(true);
                setError(null);

                const response = await fetch(
                    `${import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"}/subjects`,
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem("token")}`,
                        },
                    }
                );

                if (!response.ok) {
                    throw new Error("No se pudieron cargar las asignaturas");
                }

                const data = await response.json();
                setSubjects(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchSubjects();
    }, []);

    return (
        <div className="subjects-admin">
            <h2>Gestión de Asignaturas</h2>

            {loading && <p>Cargando asignaturas...</p>}
            {error && <p className="error">{error}</p>}

            {!loading && !error && subjects.length === 0 && (
                <p>No hay asignaturas registradas.</p>
            )}

            {!loading && !error && subjects.length > 0 && (
                <table className="subjects-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                        </tr>
                    </thead>
                    <tbody>
                        {subjects.map((s) => (
                            <tr key={s.id}>
                                <td>{s.id}</td>
                                <td>{s.name}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
``