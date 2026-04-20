import { useState } from "react";
import { calculateQuarterGrade } from "../api";
import FeedbackMessage from "./FeedbackMessage";

export default function QuarterPreview({ context }) {
    const [result, setResult] = useState(null);
    const [feedback, setFeedback] = useState(null);
    const [loading, setLoading] = useState(false);

    const isClosed = context.quarter.status === "CLOSED";

    async function handleCalculate() {
        if (isClosed) {
            setFeedback({
                type: "warning",
                message: "El Quarter está cerrado. No se puede recalcular.",
            });
            return;
        }

        setLoading(true);
        setFeedback(null);

        try {
            const res = await calculateQuarterGrade({
                student_id: 1,
                subject_id: context.subject.id,
                grade_id: context.grade.id,
                quarter_id: context.quarter.id,
                teacher_id: 1,
                academic_year: context.academicYear,
            });

            setResult(res);
            setFeedback({
                type: "success",
                message: "✅ Quarter calculado correctamente.",
            });
        } catch {
            setFeedback({
                type: "error",
                message: "❌ No se pudo calcular el Quarter.",
            });
        } finally {
            setLoading(false);
        }
    }

    return (
        <div style={{ marginTop: "2rem" }}>
            <h2>Vista previa del Quarter</h2>

            <button disabled={isClosed || loading} onClick={handleCalculate}>
                {loading ? "Calculando..." : "Calcular Quarter"}
            </button>

            <FeedbackMessage type={feedback?.type} message={feedback?.message} />

            {result && (
                <p style={{ marginTop: "1rem" }}>
                    Nota final del Quarter: <strong>{result.final_score}</strong>
                </p>
            )}
        </div>
    );
}
