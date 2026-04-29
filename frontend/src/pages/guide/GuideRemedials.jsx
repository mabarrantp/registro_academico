import { useEffect, useMemo, useState } from "react";
import { api } from "../../services/api";
import "./GuideRemedials.css";

export default function GuideRemedials() {
  const ctx = useMemo(() => ({ academicYear: 2025 }), []);

  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState("");

  const [finalGrades, setFinalGrades] = useState([]);
  const [remedials, setRemedials] = useState([]);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setMsg("");

      const [fgRes, remRes] = await Promise.allSettled([
        api.get("/final-subject-grades", { params: { academic_year: ctx.academicYear } }),
        api.get("/remedials", { params: { academic_year: ctx.academicYear } }),
      ]);

      if (fgRes.status === "fulfilled") {
        setFinalGrades(Array.isArray(fgRes.value.data) ? fgRes.value.data : []);
      } else {
        setFinalGrades([]);
        setMsg((m) => m + "⚠️ No se pudieron cargar notas anuales por materia.\n");
      }

      if (remRes.status === "fulfilled") {
        setRemedials(Array.isArray(remRes.value.data) ? remRes.value.data : []);
      } else {
        setRemedials([]);
        setMsg((m) => m + "⚠️ No se pudieron cargar exámenes de reparación.\n");
      }

      setLoading(false);
    }

    load();
  }, [ctx]);

  if (loading) return <div className="grm-loading">Cargando reparaciones…</div>;

  // Materias que requieren reparación o quedaron fallidas
  const pending = finalGrades.filter(
    (g) => g.status === "REMEDIAL" || g.status === "FAILED"
  );

  // Helper para buscar examen correspondiente
  function findExam(studentId, subjectId) {
    return remedials.find(
      (r) =>
        Number(r.student_id) === Number(studentId) &&
        Number(r.subject_id) === Number(subjectId) &&
        Number(r.academic_year) === Number(ctx.academicYear)
    );
  }

  return (
    <div className="grm-wrap">
      <div className="grm-head">
        <h1>Reparaciones</h1>
        <div className="grm-sub">Año {ctx.academicYear}</div>
      </div>

      {msg && <pre className="grm-msg">{msg}</pre>}

      {pending.length === 0 ? (
        <div className="grm-empty">✅ No hay materias pendientes de reparación.</div>
      ) : (
        <div className="grm-panel">
          <div className="grm-note">
            * Solo aparecen materias con estado <strong>REMEDIAL</strong> o <strong>FAILED</strong>.
          </div>

          <table className="grm-table">
            <thead>
              <tr>
                <th>Student ID</th>
                <th>Subject ID</th>
                <th>Nota anual</th>
                <th>Reparación</th>
                <th>Estado</th>
              </tr>
            </thead>

            <tbody>
              {pending.map((g, idx) => {
                const exam = findExam(g.student_id, g.subject_id);

                let label = "PENDIENTE";
                let cls = "pending";

                if (exam) {
                  if (Number(exam.score) >= 60) {
                    label = "APROBÓ";
                    cls = "passed";
                  } else {
                    label = "FALLÓ";
                    cls = "failed";
                  }
                }

                return (
                  <tr key={idx}>
                    <td className="strong">{g.student_id}</td>
                    <td>{g.subject_id}</td>
                    <td className="grade">{Number(g.final_grade).toFixed(2)}</td>
                    <td className="grade">{exam ? Number(exam.score).toFixed(2) : "-"}</td>
                    <td>
                      <span className={`badge ${cls}`}>{label}</span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}