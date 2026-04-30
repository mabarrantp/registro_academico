import { useEffect, useState } from "react";
import { getStudents, getFinalAverage } from "../../services/api";
import "./PromotionAdmin.css";

export default function PromotionAdmin() {
    const [students, setStudents] = useState([]);
    const [studentId, setStudentId] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function loadStudents() {
            try {
                const data = await getStudents();
                setStudents(data);
            } catch (err) {
                setError(err.message);
            }
        }

        loadStudents();
    }, []);

    const handleCheckPromotion = async () => {
        if (!studentId) return;

        try {
            setLoading(true);
            setError(null);
            setResult(null);

            const data = await getFinalAverage(studentId);
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="promotion-admin">
            <h2>Promoción de Estudiantes</h2>

            <div className="promotion-controls">
                <label>
                    Estudiante:&nbsp;
                    <select
                        value={studentId}
                        onChange={(e) => setStudentId(e.target.value)}
                    >
                        <option value="">Seleccione</option>
                        {students.map((s) => (
                            <option key={s.id} value={s.id}>
                                {s.first_name} {s.last_name}
                            </option>
                        ))}
                    </select>
                </label>

                <button
                    onClick={handleCheckPromotion}
                    disabled={!studentId || loading}
                >
                    Evaluar
                </button>
            </div>

            {loading && <p>Evaluando promoción...</p>}
            {error && <p className="error">{error}</p>}

            {result && (
                <div className="promotion-result">
                    <p>
                        <strong>Estudiante:</strong> {result.student}
                    </p>
                    <p>
                        <strong>Promedio Final:</strong>{" "}
                        {result.final_average !== null
                            ? result.final_average
                            : "-"}
                    </p>
                    <p>
                        <strong>Evaluación:</strong>{" "}
                        {result.final_qualitative}
                    </p>

                    <h3
                        className={
                            result.final_average !== null &&
                                result.final_average >= 60
                                ? "approved"
                                : "not-approved"
                        }
                    >
                        {result.final_average !== null &&
                            result.final_average >= 60
                            ? "PROMOVIDO"
                            : "NO PROMOVIDO"}
                    </h3>
                </div>
            )}
        </div>
    );
}