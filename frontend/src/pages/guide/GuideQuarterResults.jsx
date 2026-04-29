import { useEffect, useMemo, useState } from "react";
import { api } from "../../services/api";
import "./GuideQuarterResults.css";

export default function GuideQuarterResults() {
  // ⚠️ Por ahora fijo (después lo sacamos del maestro guía asignado)
  const ctx = useMemo(
    () => ({
      academicYear: 2025,
      quarterId: 1,
      passing: 60,
    }),
    []
  );

  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState("");
  const [rows, setRows] = useState([]);

  useEffect(() => {
    async function loadQuarterGrades() {
      setLoading(true);
      setMsg("");

      try {
        const res = await api.get("/quarter-grades", {
          params: {
            quarter_id: ctx.quarterId,
            academic_year: ctx.academicYear,
          },
        });

        const data = res.data;
        setRows(Array.isArray(data) ? data : []);

        if (!Array.isArray(data)) {
          setMsg("⚠️ El endpoint /quarter-grades devolvió un formato inesperado.");
        }
      } catch (e) {
        console.error(e);
        setRows([]);
        setMsg(e?.response?.data?.detail || "❌ No se pudieron cargar las notas del quarter.");
      } finally {
        setLoading(false);
      }
    }

    loadQuarterGrades();
  }, [ctx]);

  // Solo reprobadas oficiales
  const failed = rows
    .filter((r) => Number(r.final_grade) < ctx.passing)
    .sort((a, b) => Number(a.final_grade) - Number(b.final_grade));

  return (
    <div className="gq-wrap">
      <div className="gq-head">
        <h1>Resultados del Quarter</h1>
        <div className="gq-sub">
          Año {ctx.academicYear} • Quarter {ctx.quarterId} • Aprobación ≥ {ctx.passing}
        </div>
      </div>

      {loading ? (
        <div className="gq-loading">Cargando resultados oficiales…</div>
      ) : (
        <>
          {msg && <div className="gq-msg">{msg}</div>}

          {failed.length === 0 ? (
            <div className="gq-empty">
              ✅ No hay materias reprobadas oficiales en este quarter.
            </div>
          ) : (
            <div className="gq-panel">
              <div className="gq-note">
                * Estas son notas oficiales del quarter (solo después de cierre del quarter).
              </div>

              <table className="gq-table">
                <thead>
                  <tr>
                    <th>Student ID</th>
                    <th>Subject ID</th>
                    <th>Nota final</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {failed.map((r, idx) => (
                    <tr key={idx}>
                      <td className="strong">{r.student_id}</td>
                      <td>{r.subject_id}</td>
                      <td className="grade">{Number(r.final_grade).toFixed(2)}</td>
                      <td>
                        <span className="badge failed">REPROBADA</span>
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
