import { useEffect, useMemo, useState } from "react";
import { getGrades } from "../../services/api";
import "./GuideRisk.css";

export default function GuideRisk() {
    // ⚠️ Por ahora fijo. Luego lo sacamos del maestro guía asignado.
    const ctx = useMemo(
        () => ({
            academicYear: 2025,
            gradeId: 8,
            sectionId: 1,
            quarterId: 1,
        }),
        []
    );

    const [grades, setGrades] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchRiskStudents() {
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

        fetchRiskStudents();
    }, [ctx]);

    return (
        <div className="guide-risk">
            <h2>Estudiantes en Riesgo Académico</h2>

            {loading && <p>Cargando información...</p>}

            {error && <p className="error">{error}</p>}

            {!loading && !error && grades.length === 0 && (
                <p>No hay estudiantes en riesgo.</p>
            )}

            {!loading && !error && grades.length > 0 && (
                <table className="risk-table">
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
