import { useEffect, useState } from "react";
import {
    getStudents,
    getAssessmentCategories,
    createAssessment,
} from "../api";
import FeedbackMessage from "./FeedbackMessage";

export default function AssessmentRegister({ context }) {
    const [students, setStudents] = useState([]);
    const [categories, setCategories] = useState([]);
    const [scores, setScores] = useState({});
    const [feedback, setFeedback] = useState(null);

    const isClosed = context.quarter.status === "CLOSED";

    useEffect(() => {
        getStudents().then(setStudents);
        getAssessmentCategories().then(setCategories);
    }, []);

    function handleChange(studentId, value) {
        setScores({ ...scores, [studentId]: value });
    }

    async function handleSave(category) {
        if (isClosed) {
            setFeedback({
                type: "warning",
                message: "El Quarter está cerrado. No se pueden registrar actividades.",
            });
            return;
        }

        if (Object.keys(scores).length === 0) {
            setFeedback({
                type: "info",
                message: "No hay notas ingresadas para guardar.",
            });
            return;
        }

        try {
            for (const studentId in scores) {
                await createAssessment({
                    student_id: Number(studentId),
                    subject_id: context.subject.id,
                    teacher_id: 1,
                    grade_id: context.grade.id,
                    quarter_id: context.quarter.id,
                    category_id: category.id,
                    score: Number(scores[studentId]),
                });
            }

            setScores({});
            setFeedback({
                type: "success",
                message: `✅ ${category.code} guardado correctamente.`,
            });
        } catch {
            setFeedback({
                type: "error",
                message: "❌ Ocurrió un error al guardar las notas.",
            });
        }
    }

    return (
        <div>
            <h2>Registro de actividades</h2>

            <FeedbackMessage type={feedback?.type} message={feedback?.message} />

            {categories.map((cat) => (
                <div key={cat.id} style={{ marginBottom: "1.5rem" }}>
                    <h3>{cat.code}</h3>

                    {students.map((s) => (
                        <div key={s.id}>
                            {s.first_name} {s.last_name}
                            <input
                                type="number"
                                disabled={isClosed}
                                value={scores[s.id] || ""}
                                onChange={(e) => handleChange(s.id, e.target.value)}
                                style={{ marginLeft: "1rem" }}
                            />
                        </div>
                    ))}

                    <button disabled={isClosed} onClick={() => handleSave(cat)}>
                        Guardar {cat.code}
                    </button>
                </div>
            ))}
        </div>
    );
}