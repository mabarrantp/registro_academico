import { useState } from "react";
import { getReportCard } from "../api";
import FeedbackMessage from "./FeedbackMessage";

export default function ReportCard({ context }) {
    const [data, setData] = useState(null);
    const [feedback, setFeedback] = useState(null);

    async function handleLoad() {
        setFeedback({ type: "info", message: "Cargando boletín..." });

        try {
            const res = await getReportCard({
                student_id: 1,
                subject_id: context.subjectId,
                academic_year: context.academicYear,
            });
            setData(res);
            setFeedback(null);
        } catch {
            setFeedback({
                type: "warning",
                message: "ℹ️ Aún no hay boletín disponible para este contexto.",
            });
        }
    }

    return (
        <div style={{ marginTop: "2rem" }}>
            <h2>Boletín</h2>

            <button onClick={handleLoad}>Ver boletín</button>

            <FeedbackMessage type={feedback?.type} message={feedback?.message} />

            {data && (
                <table style={{ marginTop: "1rem", width: "100%" }}>
                    <thead>
                        <tr>
                            <th>QI</th>
                            <th>QII</th>
                            <th>QIII</th>
                            <th>QIV</th>
                            <th>Final</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>{data.quarters?.QI ?? "-"}</td>
                            <td>{data.quarters?.QII ?? "-"}</td>
                            <td>{data.quarters?.QIII ?? "-"}</td>
                            <td>{data.quarters?.QIV ?? "-"}</td>
                            <td><strong>{data.final_grade ?? "-"}</strong></td>
                        </tr>
                    </tbody>
                </table>
            )}
        </div>
    );
}