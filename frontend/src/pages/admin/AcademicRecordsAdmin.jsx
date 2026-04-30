import { useEffect, useState } from "react";
import { getStudents, getAcademicYears, getReportCard, downloadReportCardPDF } from "../../services/api";
import "./AcademicRecordsAdmin.css";

function AcademicRecordsAdmin() {
    const [students, setStudents] = useState([]);
    const [years, setYears] = useState([]);
    const [studentId, setStudentId] = useState("");
    const [year, setYear] = useState("");
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        Promise.all([getStudents(), getAcademicYears()])
            .then(([s, y]) => { setStudents(s); setYears(y); })
            .catch((e) => setError(e.message));
    }, []);

    const loadReport = async () => {
        try {
            setLoading(true);
            setError(null);
            const data = await getReportCard(studentId, year);
            setReport(data);
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="academic-records-admin">
            <h2>Boletín Académico</h2>

            <select value={studentId} onChange={(e) => setStudentId(e.target.value)}>
                <option value="">Estudiante</option>
                {students.map(s => <option key={s.id} value={s.id}>{s.first_name} {s.last_name}</option>)}
            </select>

            <select value={year} onChange={(e) => setYear(e.target.value)}>
                <option value="">Año</option>
                {years.map(y => <option key={y.id} value={y.year}>{y.year}</option>)}
            </select>

            <button onClick={loadReport} disabled={!studentId || !year}>Consultar</button>

            {loading && <p>Cargando...</p>}
            {error && <p className="error">{error}</p>}

            {report && (
                <>
                    <table className="records-table">
                        <thead>
                            <tr><th>Asignatura</th><th>Q1</th><th>Q2</th><th>Q3</th><th>Q4</th><th>Final</th></tr>
                        </thead>
                        <tbody>
                            {report.report_card.map((r, i) => (
                                <tr key={i}>
                                    <td>{r.subject}</td>
                                    {["Q1", "Q2", "Q3", "Q4"].map(q => (
                                        <td key={q}>{r.quarters[q]?.quantitative ?? "-"}<br /><small>{r.quarters[q]?.qualitative}</small></td>
                                    ))}
                                    <td>{r.final_average}<br /><small>{r.final_qualitative}</small></td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                    <button onClick={() => downloadReportCardPDF(studentId, year)}>Descargar PDF</button>
                </>
            )}
        </div>
    );
}

export default AcademicRecordsAdmin;
``