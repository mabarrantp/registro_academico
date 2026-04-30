import { useEffect, useState } from "react";

export default function TeachersAtRisk() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const API_URL =
        import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

    useEffect(() => {
        async function loadTeachersAtRisk() {
            try {
                const response = await fetch(
                    `${API_URL}/dashboard/coordination/teachers-at-risk`,
                    {
                        method: "GET",
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem("token")}`,
                            "Content-Type": "application/json",
                        },
                    }
                );

                if (!response.ok) {
                    throw new Error("Error al obtener docentes en riesgo");
                }

                const result = await response.json();
                setData(result);
            } catch (err) {
                console.error(err);
                setError("No se pudo cargar la información de riesgo");
            } finally {
                setLoading(false);
            }
        }

        loadTeachersAtRisk();
    }, []);

    if (loading) {
        return <p>Cargando docentes con estudiantes en riesgo...</p>;
    }

    if (error) {
        return <p style={{ color: "red" }}>{error}</p>;
    }

    return (
        <div>
            <h2>Docentes con Estudiantes en Riesgo</h2>

            {data.length === 0 ? (
                <p>No hay docentes con estudiantes en riesgo.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Docente</th>
                            <th>Grado</th>
                            <th>Estudiantes en Riesgo</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.map((item, index) => (
                            <tr key={index}>
                                <td>{item.teacher_name}</td>
                                <td>{item.grade}</td>
                                <td>{item.students_at_risk}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
