import { useEffect, useState } from "react";
import Can from "../../components/Can";

export default function EnrollmentsAdmin() {
    const [enrollments, setEnrollments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const API_URL =
        import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

    useEffect(() => {
        async function loadEnrollments() {
            try {
                const response = await fetch(`${API_URL}/enrollments`, {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                        "Content-Type": "application/json",
                    },
                });

                if (!response.ok) {
                    throw new Error("Error al obtener matrículas");
                }

                const data = await response.json();
                setEnrollments(data);
            } catch (err) {
                console.error(err);
                setError("No se pudo cargar la lista de matrículas");
            } finally {
                setLoading(false);
            }
        }

        loadEnrollments();
    }, []);

    if (loading) {
        return <p>Cargando matrículas…</p>;
    }

    if (error) {
        return <p style={{ color: "red" }}>{error}</p>;
    }

    return (
        <div>
            <h2>Matrículas</h2>

            {/* Acción futura: crear matrícula */}
            <Can permission="create">
                <button
                    className="btn btn-primary"
                    style={{ marginBottom: "16px" }}
                >
                    Nueva Matrícula
                </button>
            </Can>

            {enrollments.length === 0 ? (
                <p>No hay matrículas registradas.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Estudiante</th>
                            <th>Grado</th>
                            <th>Sección</th>
                            <th>Año Académico</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {enrollments.map((enrollment) => (
                            <tr key={enrollment.id}>
                                <td>{enrollment.student_name}</td>
                                <td>{enrollment.grade}</td>
                                <td>{enrollment.section}</td>
                                <td>{enrollment.academic_year}</td>
                                <td>
                                    <Can permission="edit">
                                        <button className="btn btn-secondary">
                                            Editar
                                        </button>
                                    </Can>

                                    <Can permission="delete">
                                        <button className="btn btn-danger">
                                            Eliminar
                                        </button>
                                    </Can>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}