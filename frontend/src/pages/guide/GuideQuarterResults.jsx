import { useEffect, useState } from "react";
import {
    getReportCard,
    downloadReportCardPDF,
} from "../../services/api";
import "./GuideQuarterResults.css";

function GuideQuarterResults() {
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // ✅ En producción real:
    // Estos valores luego vendrán de selección dinámica
    const STUDENT_ID = 1;
    const ACADEMIC_YEAR = 2026;

    useEffect(() => {
        async function fetchReportCard() {
            try {
                setLoading(true);
                setError(null);

                const data = await getReportCard(
                    STUDENT_ID,
                    ACADEMIC_YEAR
                );

                setReport(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchReportCard();
    }, []);

    const handleDownloadPDF = async () => {
        try {
            await downloadReportCardPDF(
                STUDENT_ID,
                ACADEMIC_YEAR
            );
        } catch (err) {
            alert(err.message);
        }
    };

    return (
        <div className="guide-quarter-results">
            <h2>Resultados Académicos</h2>

            {loading && <p>Cargando boletín...</p>}

            {error && <p className="error">{error}</p>}

            {!loading && !error && report && (
                <>
                    <div className="student-info">
                        <p>
                            <strong>Estudiante:</strong> {report.student}
                        </p>
                        <p>
                            <strong>Año Académico:</strong> {report.academic_year}
                        </p>
                    </div>

                    <table className="results-table">
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
                            Descargar PDF
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}

export default GuideQuarterResults;
