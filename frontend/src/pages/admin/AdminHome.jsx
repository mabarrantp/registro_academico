import { useEffect, useState } from "react";
import KpiCard from "../../components/KpiCard";

export default function AdminHome() {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);

    const API_URL =
        import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

    useEffect(() => {
        async function loadSummary() {
            try {
                const response = await fetch(
                    `${API_URL}/dashboard/admin/summary`,
                    {
                        method: "GET",
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem("token")}`,
                        },
                    }
                );

                const data = await response.json();
                setSummary(data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        }

        loadSummary();
    }, []);

    if (loading) {
        return <p>Cargando panel...</p>;
    }

    return (
        <div>
            <h1>Panel de Administración</h1>

            {/* KPI CARDS */}
            <div
                style={{
                    display: "flex",
                    gap: "20px",
                    flexWrap: "wrap",
                    marginTop: "20px",
                }}
            >
                <KpiCard
                    title="Estudiantes"
                    value={summary.total_students}
                />
                <KpiCard
                    title="Matrículas"
                    value={summary.total_enrollments}
                />
                <KpiCard
                    title="En Riesgo"
                    value={summary.students_at_risk}
                />
                <KpiCard
                    title="Promedio General"
                    value={summary.average_score}
                />
            </div>
        </div>
    );
}
