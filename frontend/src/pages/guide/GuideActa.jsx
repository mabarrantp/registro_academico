import { useEffect, useMemo, useState } from "react";
import { api } from "../../services/api";
import "./GuideActa.css";

export default function GuideActa() {
  const ctx = useMemo(
    () => ({
      academicYear: 2025,
      gradeId: 8,
      sectionId: 1,
      defaultRecordId: 1,
    }),
    []
  );

  const [recordId, setRecordId] = useState(() => {
    const saved = localStorage.getItem("academic_record_id");
    return saved ? Number(saved) : ctx.defaultRecordId;
  });

  const [loading, setLoading] = useState(true);
  const [signing, setSigning] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [msg, setMsg] = useState("");

  const [status, setStatus] = useState(null);

  async function loadStatus(id) {
    const res = await api.get("/academic-record-signatures/status", {
      params: { academic_record_id: Number(id) },
    });
    setStatus(res.data);
  }

  useEffect(() => {
    (async () => {
      setLoading(true);
      setMsg("");
      try {
        await loadStatus(recordId);
      } catch (e) {
        console.error(e);
        setMsg(e?.response?.data?.detail || "⚠️ No se pudo cargar el estado de firmas.");
      } finally {
        setLoading(false);
      }
    })();
    // eslint-disable-next-line
  }, []);

  async function handleRefresh() {
    setLoading(true);
    setMsg("");
    try {
      await loadStatus(recordId);
      setMsg("✅ Estado actualizado.");
    } catch (e) {
      console.error(e);
      setMsg(e?.response?.data?.detail || "❌ Error al actualizar estado.");
    } finally {
      setLoading(false);
    }
  }

  async function handleSign() {
    if (!recordId) return setMsg("⚠️ Indica el ID del acta.");
    if (!window.confirm("¿Confirmas firmar el acta académica?")) return;

    setSigning(true);
    setMsg("");

    try {
      await api.post("/academic-record-signatures/sign", null, {
        params: { academic_record_id: Number(recordId) },
      });
      await loadStatus(recordId);
      setMsg("✅ Acta firmada por Maestro Guía.");
    } catch (e) {
      console.error(e);
      setMsg(e?.response?.data?.detail || "❌ No se pudo firmar el acta.");
    } finally {
      setSigning(false);
    }
  }

  async function handleDownloadPdf() {
    setDownloading(true);
    setMsg("");

    try {
      const res = await api.get("/exports/academic-record/pdf", {
        params: {
          grade_id: ctx.gradeId,
          section_id: ctx.sectionId,
          academic_year: ctx.academicYear,
        },
        responseType: "blob",
      });

      const blob = new Blob([res.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = `ACTA_${ctx.gradeId}_${ctx.sectionId}_${ctx.academicYear}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();

      window.URL.revokeObjectURL(url);
      setMsg("✅ PDF descargado.");
    } catch (e) {
      console.error(e);
      setMsg("❌ No se pudo descargar el PDF.");
    } finally {
      setDownloading(false);
    }
  }

  const signedRoles = status?.signed_roles || [];
  const fullySigned = !!status?.is_fully_signed;

  const guideSigned = signedRoles.includes("GUIDE_TEACHER");
  const coordSigned = signedRoles.includes("COORDINATION");
  const directorSigned = signedRoles.includes("DIRECTOR");

  return (
    <div className="ga-wrap">
      <div className="ga-head">
        <h1>Acta Académica</h1>
        <div className="ga-sub">
          Año {ctx.academicYear} • Grado {ctx.gradeId} • Sección {ctx.sectionId}
        </div>
      </div>

      {msg && <div className="ga-msg">{msg}</div>}

      <div className="ga-panel">
        <h2>Identificador del Acta</h2>

        <div className="ga-row">
          <div className="ga-field">
            <label>Academic Record ID</label>
            <input
              type="number"
              value={recordId}
              onChange={(e) => {
                const val = Number(e.target.value || 0);
                setRecordId(val);
                localStorage.setItem("academic_record_id", String(val));
              }}
              placeholder="Ej: 1"
            />
            <div className="ga-help">
              * El Admin genera el acta y te comparte este ID.
            </div>
          </div>

          <div className="ga-actions">
            <button className="btn btn-secondary" onClick={handleRefresh} disabled={loading}>
              {loading ? "Actualizando…" : "Actualizar estado"}
            </button>
          </div>
        </div>
      </div>

      <div className="ga-panel">
        <h2>Estado de firmas</h2>

        <div className="ga-status">
          <div className="ga-status-item">
            <span>Maestro Guía</span>
            <strong className={guideSigned ? "ok" : "pending"}>
              {guideSigned ? "Firmado" : "Pendiente"}
            </strong>
          </div>

          <div className="ga-status-item">
            <span>Coordinación</span>
            <strong className={coordSigned ? "ok" : "pending"}>
              {coordSigned ? "Firmado" : "Pendiente"}
            </strong>
          </div>

          <div className="ga-status-item">
            <span>Dirección (opcional)</span>
            <strong className={directorSigned ? "ok" : "pending"}>
              {directorSigned ? "Firmado" : "—"}
            </strong>
          </div>

          <div className="ga-status-item">
            <span>Acta completa</span>
            <strong className={fullySigned ? "ok" : "pending"}>
              {fullySigned ? "Sí (bloqueada)" : "No"}
            </strong>
          </div>
        </div>

        {/* ✅ Botones estandarizados */}
        <div className="ga-actions-inline">
          {!guideSigned && !fullySigned && (
            <button className="btn btn-success" onClick={handleSign} disabled={signing}>
              {signing ? "Firmando…" : "Firmar acta"}
            </button>
          )}

          <button className="btn btn-secondary" onClick={handleDownloadPdf} disabled={downloading}>
            {downloading ? "Descargando…" : "Descargar PDF"}
          </button>
        </div>

        <div className="ga-note">
          * El Maestro Guía solo firma y descarga. Generación del acta y promoción final son funciones administrativas.
        </div>
      </div>
    </div>
  );
}
