import { useEffect, useState, useMemo } from "react";
import {
    getReportCard,
    downloadReportCardPDF,
} from "../../services/api";
import "./GuideActa.css";

export default function GuideActa() {
    // ⚠️ Contexto fijo por ahora
    // Luego se obtiene del guía autenticado
    const ctx = useMemo(
        () => ({
            studentId: 1,
            academicYear: 2026,
        }),
        []
    );

    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchActa() {
            try {
                setLoading(true);
                setError(null);

                const data = await getReportCard(
                    ctx.studentId,
                    ctx.academicYear
                );

                setReport(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchActa();
    }, [ctx]);

    const handleDownloadPDF = async () => {
        try {
            await downloadReportCardPDF(
                ctx.studentId,
                ctx.academicYear
            );
        } catch (err) {
            alert(err.message);
        }
    };

    return (
        <div className="guide-acta">
            <h2>Acta Académica</h2>

            {loading && <p>Cargando acta...</p>}

            {error && <p className="error">{error}</p>}

            {!loading && !error && report && (
                <>
                    <div className="acta-header">
                        <p>
                            <strong>Estudiante:</strong> {report.student}
                        </p>
                        <p>
                            <strong>Año Académico:</strong> {report.academic_year}
                        </p>
                    </div>

                    <table className="acta-table">
                        <thead>
                            <tr>
                                <th>Asignatura</th>
                                <th>Q1</th>
                                <th>Q2</th>
                                <th>Q3</th>
                                <th>Q4</th>
                                <th>Final</th>
                            </tr>
                        </thead>
                        <tbody>
                            {report.report_card.map((item, index) => (
                                <tr key={index}>
                                    <td>{item.subject}</td>

                                    {["Q1", "Q2", "Q3", "Q4"].map((q) => {
                                        const quarter = item.quarters[q];
                                        return (
                                            <td key={q}>
                                                {quarter && quarter.quantitative !== null
                                                    ? quarter.quantitative
                                                    : "-"}
                                                <br />
                                                <small>
                                                    {quarter ? quarter.qualitative : ""}
                                                </small>
                                            </td>
                                        );
                                    })}

                                    <td>
                                        {item.final_average !== null
                                            ? item.final_average
                                            : "-"}
                                        <br />
                                        <small>{item.final_qualitative}</small>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                    <div className="actions">
                        <button onClick={handleDownloadPDF}>
                            Descargar Acta (PDF)
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}
