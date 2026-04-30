import { useEffect, useState, useMemo } from "react";
import { getGrades } from "../../services/api";
import "./GuideRemedials.css";

export default function GuideRemedials() {
    // ⚠️ Contexto fijo por ahora (producción inicial)
    // Luego puede venir del guía autenticado
    const ctx = useMemo(
        () => ({
            sectionId: 1,
            quarterId: 1,
        }),
        []
    );

    const [grades, setGrades] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchRemedials() {
            try {
                setLoading(true);
                setError(null);

                const data = await getGrades({
                    sectionId: ctx.sectionId,
                    quarterId: ctx.quarterId,
                });

                setGrades(data.grades);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchRemedials();
    }, [ctx]);

    return (
        <div className="guide-remedials">
            <h2>Clases de Refuerzo</h2>

            {loading && <p>Cargando información...</p>}

            {error && <p className="error">{error}</p>}

            {!loading && !error && grades.length === 0 && (
                <p>No hay estudiantes que requieran refuerzo.</p>
            )}

            {!loading && !error && grades.length > 0 && (
                <table className="remedials-table">
                    <thead>
                        <tr>
                            <th>Estudiante</th>
                            <th>Asignatura</th>
                            <th>Quarter</th>
                            <th>Nota</th>
                            <th>Cualitativo</th>
                        </tr>
                    </thead>
                    <tbody>
                        {grades.map((g, index) => (
                            <tr key={index}>
                                <td>{g.student}</td>
                                <td>{g.subject}</td>
                                <td>{g.quarter}</td>
                                <td>{g.quantitative ?? "-"}</td>
                                <td>{g.qualitative}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
``