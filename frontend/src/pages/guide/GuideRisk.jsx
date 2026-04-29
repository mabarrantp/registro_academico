import { useEffect, useMemo, useState } from "react";
import { api } from "../../services/api";
import "./GuideRisk.css";

export default function GuideRisk() {
  // ⚠️ Por ahora fijo. Luego lo sacamos del maestro guía asignado.
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
  const [riskRows, setRiskRows] = useState([]);

  useEffect(() => {
    async function loadRisk() {
      setLoading(true);
      setMsg("");

      try {
        const res = await api.get("/risk", {
          params: {
            academic_year: ctx.academicYear,
            grade_id: ctx.gradeId,
            section_id: ctx.sectionId,
            quarter_id: ctx.quarterId,
          },
        });

        const data = res.data;
        setRiskRows(Array.isArray(data) ? data : []);
        if (!Array.isArray(data)) {
          setMsg("⚠️ El endpoint /risk devolvió un formato inesperado.");
        }
      } catch (e) {
        console.error(e);
        setRiskRows([]);
        setMsg(e?.response?.data?.detail || "❌ No se pudo cargar el riesgo académico.");
      } finally {
        setLoading(false);
      }
    }

    loadRisk();
  }, [ctx]);

  // Orden: primero HIGH, luego MEDIUM; y dentro por promedio ascendente
  const sorted = [...riskRows].sort((a, b) => {
    const aLevel = (a.risk_level || "").toUpperCase() === "HIGH" ? 0 : 1;
    const bLevel = (b.risk_level || "").toUpperCase() === "HIGH" ? 0 : 1;
    if (aLevel !== bLevel) return aLevel - bLevel;
    return Number(a.average || 0) - Number(b.average || 0);
  });

  return (
    <div className="gr-wrap">
      <div className="gr-head">
        <h1>Riesgo Académico</h1>
        <div className="gr-sub">
          Año {ctx.academicYear} • Grado {ctx.gradeId} • Sección {ctx.sectionId} • Quarter {ctx.quarterId}
        </div>
      </div>

      {loading ? (
        <div className="gr-loading">Cargando riesgo académico…</div>
      ) : (
        <>
          {msg && <div className="gr-msg">{msg}</div>}

          {sorted.length === 0 ? (
            <div className="gr-empty">
              ✅ No hay estudiantes en riesgo para este quarter.
            </div>
          ) : (
            <div className="gr-panel">
              <div className="gr-legend">
                <span className="pill high">ALTO (&lt; 60)</span>
                <span className="pill medium">MEDIO (60–64)</span>
                <span className="note">
                  * Este reporte es preventivo (quarter abierto). No es “reprobado oficial”.
                </span>
              </div>

              <table className="gr-table">
                <thead>
                  <tr>
                    <th>Estudiante</th>
                    <th>Materia</th>
                    <th>Promedio actual</th>
                    <th>Nivel</th>
                  </tr>
                </thead>
                <tbody>
                  {sorted.map((r, idx) => (
                    <tr key={idx}>
                      <td className="strong">{r.student || `ID ${r.student_id}`}</td>
                      <td>{r.subject || `Materia #${r.subject_id}`}</td>
                      <td>{Number(r.average).toFixed(2)}</td>
                      <td>
                        <RiskBadge level={(r.risk_level || "").toUpperCase()} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}

function RiskBadge({ level }) {
  if (level === "HIGH") return <span className="badge high">ALTO</span>;
  return <span className="badge medium">MEDIO</span>;
}
