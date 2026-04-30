import { useEffect, useState } from "react";
import KpiCard from "../../components/KpiCard";
import AverageByGradeChart from "./AverageByGradeChart";
import TeachersAtRisk from "./TeachersAtRisk";
import Can from "../../components/Can";

export default function CoordinationDashboard() {
    const [summary, setSummary] = useState(null);
    const API_URL =
        import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

    useEffect(() => {
        async function loadSummary() {
            const response = await fetch(
                `${API_URL}/dashboard/coordination/summary`,
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    },
                }
            );

            const data = await response.json();
            setSummary(data);
        }

        loadSummary();
    }, []);

    if (!summary) return <p>Cargando dashboard...</p>;

    return (
        <div>
            <h1>Dashboard de Coordinación</h1>

            {/* KPI CARDS */}
            <div
                style={{
                    display: "flex",
                    gap: "20px",
                    flexWrap: "wrap",
                    marginBottom: "30px",
                }}
            >
                <KpiCard title="Estudiantes" value={summary.total_students} />
                <KpiCard title="Promedio General" value={summary.average_score} />
                <KpiCard
                    title="Docentes en Riesgo"
                    value={summary.teachers_at_risk}
                />
            </div>

            <section>
                <h3>Promedio por Grado</h3>
                <AverageByGradeChart />
            </section>

            <section style={{ marginTop: "30px" }}>
                <h3>Docentes con Estudiantes en Riesgo</h3>
                <TeachersAtRisk />
            </section>

            <Can permission="export">
                <button className="btn btn-outline" style={{ marginTop: "20px" }}>
                    Exportar Reporte
                </button>
            </Can>
        </div>
    );
}
``