import { useState } from "react";
import { closeQuarter } from "../api.js";

export default function CloseQuarterButton({ quarter, onClosed }) {
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState(null);

  if (!quarter) return null;
  if (quarter.status === "CLOSED") return null;

  async function handleClose() {
    const ok = window.confirm(
      `¿Cerrar el Quarter ${quarter.code}? Esta acción bloquea cambios.`
    );
    if (!ok) return;

    setLoading(true);
    setMsg(null);

    try {
      const updated = await closeQuarter(quarter.id);
      setMsg({ type: "success", text: `✅ ${updated.code} cerrado.` });
      onClosed(updated);
    } catch (e) {
      setMsg({ type: "error", text: `❌ ${e.message}` });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h3>Acciones de Coordinación</h3>

      <button onClick={handleClose} disabled={loading}>
        {loading ? "Cerrando..." : `Cerrar ${quarter.code}`}
      </button>

      {msg && (
        <div className={`feedback ${msg.type}`} style={{ marginTop: "1rem" }}>
          {msg.text}
        </div>
      )}
    </div>
  );
}