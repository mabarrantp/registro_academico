import { useEffect, useMemo, useState } from "react";
import { api } from "../../services/api";
import "./GuideHome.css";

export default function GuideHome() {
  // ⚠️ Por ahora está fijo. Luego lo leeremos del maestro guía asignado.
  const ctx = useMemo(
    () => ({
      academicYear: 2025,
      gradeId: 8,
      sectionId: 1,
      quarterId: 1,
    }),
    []
  );

  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState("");

  const [students, setStudents] = useState([]);
  const [risk, setRisk] = useState([]);
  const [promotion, setPromotion] = useState([]);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setMsg("");

      const [stRes, riskRes, promoRes] = await Promise.allSettled([
        api.get("/students", {
          params: {
            academic_year: ctx.academicYear,
            grade_id: ctx.gradeId,
            section_id: ctx.sectionId,
          },
        }),
        api.get("/risk", {
          params: {
            academic_year: ctx.academicYear,
            grade_id: ctx.gradeId,
            section_id: ctx.sectionId,
            quarter_id: ctx.quarterId,
          },
        }),
        api.get("/promotion/results", {
          params: {
            academic_year: ctx.academicYear,
            grade_id: ctx.gradeId,
            section_id: ctx.sectionId,
          },
        }),
      ]);

      // Students
      if (stRes.status === "fulfilled") {
        setStudents(Array.isArray(stRes.value.data) ? stRes.value.data : []);
      } else {
        setStudents([]);
        setMsg((m) => m + "⚠️ No se pudieron cargar estudiantes.\n");
      }

      // Risk
      if (riskRes.status === "fulfilled") {
        setRisk(Array.isArray(riskRes.value.data) ? riskRes.value.data : []);
      } else {
        setRisk([]);
        setMsg((m) => m + "⚠️ No se pudo cargar riesgo académico.\n");
      }

      // Promotion results (puede estar vacío si aún no se ha ejecutado promoción)
      if (promoRes.status === "fulfilled") {
        setPromotion(Array.isArray(promoRes.value.data) ? promoRes.value.data : []);
      } else {
        setPromotion([]);
        // esto no es crítico para el resumen diario
      }

      setLoading(false);
    }

    load();
  }, [ctx]);

  if (loading) {
    return <div className="gh-loading">Cargando resumen…</div>;
  }

  const totalStudents = students.length;
  const studentsInRisk = new Set(risk.map((r) => r.student_id)).size;

  const promoted = promotion.filter((p) => p.status === "PROMOTED").length;
  const retained = promotion.filter((p) => p.status === "RETAINED").length;

  return (
    <div className="gh-wrap">
      <div className="gh-head">
        <h1>Resumen del Grupo</h1>
        <div className="gh-sub">
          Año {ctx.academicYear} • Grado {ctx.gradeId} • Sección {ctx.sectionId}
        </div>
      </div>

      {msg && <pre className="gh-msg">{msg}</pre>}

      <div className="gh-cards">
        <StatCard label="Total estudiantes" value={totalStudents} tone="blue" />
        <StatCard label="En riesgo (Q abierto)" value={studentsInRisk} tone="orange" />
        <StatCard label="Promovidos (fin de año)" value={promoted} tone="green" />
        <StatCard label="Retenidos (fin de año)" value={retained} tone="red" />
      </div>

      <div className="gh-panel">
        <h2>Estudiantes</h2>

        {students.length === 0 ? (
          <div className="gh-empty">No hay estudiantes para este grupo.</div>
        ) : (
          <table className="gh-table">
            <thead>
              <tr>
                <th>Estudiante</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {students.map((s) => {
                const hasRisk = risk.some((r) => r.student_id === s.id);
                const promo = promotion.find((p) => p.student_id === s.id);

                let status = "✅ Bien";
                if (promo?.status === "RETAINED") status = "❌ Retenido";
                else if (hasRisk) status = "⚠️ En riesgo";

                return (
                  <tr key={s.id}>
                    <td>{s.first_name} {s.last_name}</td>
                    <td>{status}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

function StatCard({ label, value, tone }) {
  return (
    <div className={`gh-card ${tone || ""}`}>
      <div className="gh-card-value">{value}</div>
      <div className="gh-card-label">{label}</div>
    </div>
  );
}
