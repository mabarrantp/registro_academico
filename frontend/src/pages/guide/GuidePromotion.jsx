import { useEffect, useMemo, useState } from "react";
import { getFinalAverage } from "../../services/api";
import "./GuidePromotion.css";

export default function GuidePromotion() {
    // ⚠️ Contexto fijo por ahora
    // Luego se obtiene del guía autenticado
    const ctx = useMemo(
        () => ({
            studentId: 1,
        }),
        []
    );

    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchPromotionStatus() {
            try {
                setLoading(true);
                setError(null);

                const data = await getFinalAverage(ctx.studentId);
                setResult(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchPromotionStatus();
    }, [ctx]);

    return (
        <div className="guide-promotion">
            <h2>Estado de Promoción</h2>

            {loading && <p>Evaluando promoción...</p>}

            {error && <p className="error">{error}</p>}

            {!loading && !error && result && (
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
``