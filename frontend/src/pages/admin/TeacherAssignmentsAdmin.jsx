import { useEffect, useState } from "react";
import "./TeachersAssignmentsAdmin.css";

export default function TeachersAssignmentsAdmin() {
    const [teachers, setTeachers] = useState([]);
    const [subjects, setSubjects] = useState([]);
    const [sections, setSections] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function loadData() {
            try {
                setLoading(true);
                setError(null);

                const baseUrl =
                    import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

                const headers = {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                };

                const [teachersRes, subjectsRes, sectionsRes] = await Promise.all([
                    fetch(`${baseUrl}/teachers`, { headers }),
                    fetch(`${baseUrl}/subjects`, { headers }),
                    fetch(`${baseUrl}/sections`, { headers }),
                ]);

                if (!teachersRes.ok || !subjectsRes.ok || !sectionsRes.ok) {
                    throw new Error("Error cargando datos para asignaciones");
                }

                const teachersData = await teachersRes.json();
                const subjectsData = await subjectsRes.json();
                const sectionsData = await sectionsRes.json();

                setTeachers(teachersData);
                setSubjects(subjectsData);
                setSections(sectionsData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        loadData();
    }, []);

    return (
        <div className="teachers-assignments-admin">
            <h2>Asignación de Docentes</h2>

            {loading && <p>Cargando información...</p>}
            {error && <p className="error">{error}</p>}

            {!loading && !error && (
                <>
                    <div className="assignments-section">
                        <h3>Docentes</h3>
                        <ul>
                            {teachers.map((t) => (
                                <li key={t.id}>
                                    {t.first_name} {t.last_name}
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="assignments-section">
                        <h3>Asignaturas</h3>
                        <ul>
                            {subjects.map((s) => (
                                <li key={s.id}>{s.name}</li>
                            ))}
                        </ul>
                    </div>

                    <div className="assignments-section">
                        <h3>Secciones</h3>
                        <ul>
                            {sections.map((sec) => (
                                <li key={sec.id}>{sec.label}</li>
                            ))}
                        </ul>
                    </div>

                    {/* 
            Nota:
            La lógica de asignación (guardar relaciones)
            se conecta después sin romper esta estructura.
          */}
                </>
            )}
        </div>
    );
}
