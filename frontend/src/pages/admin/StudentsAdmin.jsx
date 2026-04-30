import { useEffect, useState } from "react";
import Can from "../../components/Can";
import { downloadExcel } from "../../utils/downloadExcel";
import { auditAction } from "../../utils/audit";

export default function StudentsAdmin() {
    const [students, setStudents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const API_URL =
        import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

    useEffect(() => {
        async function loadStudents() {
            try {
                const response = await fetch(`${API_URL}/students`, {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    },
                });

                if (!response.ok) {
                    throw new Error("Error al obtener estudiantes");
                }

                const data = await response.json();
                setStudents(data);
            } catch (err) {
                console.error(err);
                setError("No se pudo cargar la lista de estudiantes");
            } finally {
                setLoading(false);
            }
        }

        loadStudents();
    }, []);

    async function handleExport() {
        try {
            await downloadExcel(
                `${API_URL}/reports/students/export`,
                "estudiantes.xlsx"
            );

            // ✅ Auditoría
            auditAction("EXPORT_STUDENTS", "Students");
        } catch (err) {
            console.error(err);
            alert("Error al exportar estudiantes");
        }
    }

    if (loading) {
        return <p>Cargando estudiantes…</p>;
    }

    if (error) {
        return <p style={{ color: "red" }}>{error}</p>;
    }

    return (
        <div>
            <h2>Estudiantes</h2>

            <Can permission="export">
                <button
                    className="btn btn-outline"
                    style={{ marginBottom: "16px" }}
                    onClick={handleExport}
                >
                    Exportar Excel
                </button>
            </Can>

            {students.length === 0 ? (
                <p>No hay estudiantes registrados.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Grado</th>
                            <th>Sección</th>
                        </tr>
                    </thead>
                    <tbody>
                        {students.map((s) => (
                            <tr key={s.id}>
                                <td>{s.full_name}</td>
                                <td>{s.grade}</td>
                                <td>{s.section}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}