import { useEffect, useState } from "react";
import { getStudents } from "../../services/api";
import "./GuideHome.css";

function GuideHome() {
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchStudents() {
            try {
                setLoading(true);
                setError(null);

                const data = await getStudents();
                setStudents(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchStudents();
    }, []);

    return (
        <div className="guide-home">
            <h2>Inicio – Guía Académico</h2>

            {loading && <p>Cargando información...</p>}
            {error && <p className="error">{error}</p>}

            {!loading && !error && (
                <div>
                    <p>Estudiantes asignados:</p>
                    <ul>
                        {students.map((s) => (
                            <li key={s.id}>
                                {s.first_name} {s.last_name}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default GuideHome;
