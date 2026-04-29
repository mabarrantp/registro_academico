import { useEffect, useMemo, useState } from "react";
import { api } from "../../services/api";
import "./GuidePromotion.css";

export default function GuidePromotion() {
  // ?? Por ahora fijo. Luego vendrá del maestro guía asignado.
  const ctx = useMemo(
    () => ({
      academicYear: 2025,
      gradeId: 8,
      sectionId: 1,
    }),
    []
  );

  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState("");
  const [rows, setRows] = useState([]);

  useEffect(() => {
    async function loadResults() {
      setLoading(true);
      setMsg("");

      try {
        const res = await api.get("/promotion/results", {
          params: {
            academic_year: ctx.academicYear,
            grade_id: ctx.gradeId,
            section_id: ctx.sectionId,
          },
        });

        const data = res.data;
        setRows(Array.isArray(data) ? data : []);

        if (!Array.isArray(data)) {
          setMsg("?? El endpoint /promotion/results devolvió un formato inesperado.");
        }
      } catch (e) {
        console.error(e);
        setRows([]);
        setMsg(e?.response?.data?.detail || "? No se pudieron cargar resultados de promoción.");
      } finally {
        setLoading(false);
      }
    }

    loadResults();
  }, [ctx]);

  // Conteos para resumen
  const promoted = rows.filter((r) => String(r.status).toUpperCase() === "PROMOTED").length;
  const retained = rows.filter((r) => String(r.status).toUpperCase() === "RETAINED").length;

  // Orden: Retained primero, luego Promoted; dentro por reprobadas desc
  const sorted = [...rows].sort((a, b) => {
    const aKey = String(a.status).toUpperCase() === "RETAINED" ? 0 : 1;
    const bKey = String(b.status).toUpperCase() === "RETAINED" ? 0 : 1;
    if (aKey !== bKey) return aKey - bKey;
    return Number(b.failed_subjects || 0) - Number(a.failed_subjects || 0);
  });

  return (
    <div className="gp-wrap">
      <div className="gp-head">
        <h1>Promoción Final</h1>
        <div className="gp-sub">
          Año {ctx.academicYear} • Grado {ctx.gradeId} • Sección {ctx.sectionId}
        </div>
      </div>

      {loading ? (
        <div className="gp-loading">Cargando resultados…</div>
      ) : (
        <>
          {msg && <div className="gp-msg">{msg}</div>}

          <div className="gp-cards">
            <StatCard label="Promovidos" value={promoted} tone="green" />
            <StatCard label="Retenidos" value={retained} tone="red" />
            <StatCard label="Total" value={rows.length} tone="blue" />
          </div>

          {sorted.length === 0 ? (
            <div className="gp-empty">
              No hay resultados aún. (¿Ya ejecutaron la promoción final?)
            </div>
          ) : (
            <div className="gp-panel">
              <div className="gp-note">
                * Resultado oficial del cierre anual. El Maestro Guía solo visualiza.
              </div>

              <table className="gp-table">
                <thead>
                  <tr>
                    <th>Estudiante</th>
                    <th>Reprobadas</th>
                    <th>Resultado</th>
                  </tr>
                </thead>
                <tbody>
                  {sorted.map((r, idx) => {
                    const status = String(r.status).toUpperCase();
                    return (
                      <tr key={idx}>
                        <td className="strong">{r.student_name || r.local_code || r.student_id}</td>
                        <td className="grade">{Number(r.failed_subjects || 0)}</td>
                        <td>
                          {status === "PROMOTED" ? (
                            <span className="badge promoted">PROMOVIDO</span>
                          ) : (
                            <span className="badge retained">RETENIDO</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}

function StatCard({ label, value, tone }) {
  return (
    <div className={`gp-card ${tone || ""}`}>
      <div className="gp-card-value">{value}</div>
      <div className="gp-card-label">{label}</div>
    </div>
  );
}