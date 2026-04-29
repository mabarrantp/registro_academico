import { useEffect, useMemo, useState } from "react";
import { api } from "../../services/api";
import "./PromotionAdmin.css";

export default function PromotionAdmin() {
  const ctx = useMemo(() => ({ academicYear: 2025 }), []);

  const [loading, setLoading] = useState(false);
  const [running, setRunning] = useState(false);
  const [message, setMessage] = useState("");

  const [results, setResults] = useState([]);

  async function runPromotion() {
    const ok = window.confirm(
      "¿Confirmas ejecutar la promoción final?\n\nEsta acción es DEFINITIVA."
    );
    if (!ok) return;

    setRunning(true);
    setMessage("");

    try {
      await api.post("/promotion/run", null, {
        params: { academic_year: ctx.academicYear },
      });
      setMessage("✅ Promoción ejecutada correctamente.");
      await loadResults();
    } catch (err) {
      console.error(err);
      setMessage(
        err?.response?.data?.detail || "❌ Error al ejecutar la promoción."
      );
    } finally {
      setRunning(false);
    }
  }

  async function loadResults() {
    setLoading(true);
    setMessage("");

    try {
      const res = await api.get("/promotion/results", {
        params: { academic_year: ctx.academicYear },
      });
      setResults(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error(err);
      setResults([]);
      setMessage(
        err?.response?.data?.detail || "❌ No se pudieron cargar resultados."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadResults();
    // eslint-disable-next-line
  }, []);

  const promoted = results.filter((r) => r.status === "PROMOTED").length;
  const retained = results.filter((r) => r.status === "RETAINED").length;

  return (
    <div className="promotion-admin">
      <h1>Promoción Final</h1>
      <p className="subtitle">
        Cierre anual y resultados oficiales • Año {ctx.academicYear}
      </p>

      {message && <div className="message">{message}</div>}

      <div className="panel">
        <h2>Ejecutar promoción</h2>

        <div className="actions">
          <button
            className="btn btn-danger"
            onClick={runPromotion}
            disabled={running}
          >
            {running ? "Ejecutando…" : "Ejecutar Promoción"}
          </button>

          <button
            className="btn btn-secondary"
            onClick={loadResults}
            disabled={loading}
          >
            {loading ? "Cargando…" : "Refrescar Resultados"}
          </button>
        </div>
      </div>

      <div className="panel">
        <h2>Resumen</h2>

        <div className="summary">
          <div>
            <span>Promovidos</span>
            <strong className="ok">{promoted}</strong>
          </div>
          <div>
            <span>Retenidos</span>
            <strong className="bad">{retained}</strong>
          </div>
          <div>
            <span>Total</span>
            <strong>{results.length}</strong>
          </div>
        </div>
      </div>

      <div className="panel">
        <h2>Resultados detallados</h2>

        {loading ? (
          <div className="loading">Cargando resultados…</div>
        ) : results.length === 0 ? (
          <div className="empty">No hay resultados para este año.</div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Estudiante</th>
                <th>Reprobadas</th>
                <th>Resultado</th>
              </tr>
            </thead>
            <tbody>
              {results.map((r, i) => (
                <tr key={i}>
                  <td className="strong">
                    {r.student_name || r.student_id}
                  </td>
                  <td>{r.failed_subjects}</td>
                  <td>
                    <span
                      className={`badge ${
                        r.status === "PROMOTED" ? "open" : "closed"
                      }`}
                    >
                      {r.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        <div className="hint">
          * Una vez ejecutada la promoción, los resultados son oficiales.
        </div>
      </div>
    </div>
  );
}