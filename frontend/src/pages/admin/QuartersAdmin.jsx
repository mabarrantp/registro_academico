import { useEffect, useMemo, useState } from "react";
import { api } from "../../services/api";
import "./QuartersAdmin.css";

export default function QuartersAdmin() {
  const ctx = useMemo(() => ({ academicYear: 2025 }), []);

  const [quarters, setQuarters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState(null);
  const [message, setMessage] = useState("");

  async function loadQuarters() {
    setLoading(true);
    setMessage("");

    try {
      const res = await api.get("/quarters");
      const data = Array.isArray(res.data) ? res.data : [];

      const filtered = data.filter((q) =>
        q?.academic_year ? Number(q.academic_year) === Number(ctx.academicYear) : true
      );

      filtered.sort((a, b) => (a.order ?? a.id) - (b.order ?? b.id));

      setQuarters(filtered);
    } catch (err) {
      console.error(err);
      setQuarters([]);
      setMessage(err?.response?.data?.detail || "❌ No se pudieron cargar los quarters.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadQuarters();
    // eslint-disable-next-line
  }, []);

  async function closeQuarter(q) {
    const label = q.code || `Q${q.order || q.id}`;
    const ok = window.confirm(`¿Confirmas cerrar ${label}?`);
    if (!ok) return;

    setBusyId(q.id);
    setMessage("");

    try {
      await api.post(`/quarters/${q.id}/close`);
      setMessage(`✅ Quarter ${label} cerrado.`);
      await loadQuarters();
    } catch (err) {
      console.error(err);
      setMessage(err?.response?.data?.detail || "❌ No se pudo cerrar el quarter.");
    } finally {
      setBusyId(null);
    }
  }

  async function openQuarter(q) {
    const label = q.code || `Q${q.order || q.id}`;
    const ok = window.confirm(`¿Confirmas reabrir ${label}?`);
    if (!ok) return;

    setBusyId(q.id);
    setMessage("");

    try {
      await api.post(`/quarters/${q.id}/open`);
      setMessage(`✅ Quarter ${label} reabierto.`);
      await loadQuarters();
    } catch (err) {
      console.error(err);
      setMessage(err?.response?.data?.detail || "❌ No se pudo reabrir el quarter.");
    } finally {
      setBusyId(null);
    }
  }

  const statusLabel = (status) => String(status || "").toUpperCase();

  return (
    <div className="quarters-admin">
      <h1>Quarters</h1>
      <p className="subtitle">Control de apertura/cierre • Año {ctx.academicYear}</p>

      <div className="panel">
        <div className="filter-row">
          <div className="field">
            <label>Año académico</label>
            <input type="number" value={ctx.academicYear} disabled />
          </div>

          <div className="actions">
            <button className="btn btn-secondary" onClick={loadQuarters} disabled={loading}>
              {loading ? "Cargando…" : "Refrescar"}
            </button>
          </div>
        </div>

        {message && <div className="message">{message}</div>}
      </div>

      {loading ? (
        <div className="loading">Cargando quarters…</div>
      ) : quarters.length === 0 ? (
        <div className="empty">No hay quarters para el año seleccionado.</div>
      ) : (
        <div className="panel">
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Quarter</th>
                <th>Año</th>
                <th>Estado</th>
                <th style={{ width: 260 }}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {quarters.map((q) => {
                const label = q.code || `Q${q.order || q.id}`;
                const status = statusLabel(q.status);
                const isOpen = status === "OPEN";
                const isBusy = busyId === q.id;

                return (
                  <tr key={q.id}>
                    <td>{q.id}</td>
                    <td>{label}</td>
                    <td>{q.academic_year ?? ctx.academicYear}</td>
                    <td>
                      <span className={`badge ${isOpen ? "open" : "closed"}`}>
                        {status || "N/A"}
                      </span>
                    </td>
                    <td className="row-actions">
                      {isOpen ? (
                        <button
                          className="btn btn-danger"
                          onClick={() => closeQuarter(q)}
                          disabled={isBusy}
                        >
                          {isBusy ? "Procesando…" : "Cerrar"}
                        </button>
                      ) : (
                        <button
                          className="btn btn-primary"
                          onClick={() => openQuarter(q)}
                          disabled={isBusy}
                        >
                          {isBusy ? "Procesando…" : "Reabrir"}
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          <div className="hint">
            * Cerrar quarter congela resultados oficiales. Reabrir permite correcciones (solo Admin/Coordinación).
          </div>
        </div>
      )}
    </div>
  );
}
