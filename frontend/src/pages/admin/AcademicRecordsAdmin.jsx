import { useEffect, useMemo, useState } from "react";
import { api } from "../../services/api";
import "./AcademicRecordsAdmin.css";

export default function AcademicRecordsAdmin() {
  const ctx = useMemo(() => ({ academicYear: 2025 }), []);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const [grades, setGrades] = useState([]);
  const [sections, setSections] = useState([]);

  const [gradeId, setGradeId] = useState("");
  const [sectionId, setSectionId] = useState("");
  const [recordId, setRecordId] = useState("");

  const [status, setStatus] = useState(null);

  useEffect(() => {
    loadCatalogs();
    // eslint-disable-next-line
  }, []);

  async function loadCatalogs() {
    try {
      const [gRes, sRes] = await Promise.all([
        api.get("/grades"),
        api.get("/sections"),
      ]);

      setGrades(gRes.data || []);
      setSections(
        (sRes.data || []).filter(
          (s) => !s.academic_year || s.academic_year === ctx.academicYear
        )
      );
    } catch (err) {
      console.error(err);
      setMessage("❌ Error cargando catálogos.");
    }
  }

  async function generateRecord() {
    if (!gradeId || !sectionId) {
      setMessage("⚠️ Selecciona grado y sección.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const res = await api.post("/academic-records/generate", null, {
        params: {
          grade_id: Number(gradeId),
          section_id: Number(sectionId),
          academic_year: ctx.academicYear,
        },
      });

      setRecordId(res.data.academic_record_id);
      setMessage("✅ Acta académica generada.");
    } catch (err) {
      console.error(err);
      setMessage(
        err?.response?.data?.detail || "❌ No se pudo generar el acta."
      );
    } finally {
      setLoading(false);
    }
  }

  async function checkStatus() {
    if (!recordId) {
      setMessage("⚠️ Ingresa un Academic Record ID.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const res = await api.get("/academic-record-signatures/status", {
        params: { academic_record_id: Number(recordId) },
      });

      setStatus(res.data);
      setMessage("✅ Estado de firmas cargado.");
    } catch (err) {
      console.error(err);
      setStatus(null);
      setMessage(
        err?.response?.data?.detail || "❌ No se pudo consultar el estado."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="ar-admin">
      <h1>Actas Académicas</h1>
      <p className="subtitle">
        Generación y seguimiento de firmas oficiales • Año {ctx.academicYear}
      </p>

      {message && <div className="message">{message}</div>}

      {/* GENERAR ACTA */}
      <div className="panel">
        <h2>Generar Acta</h2>

        <div className="grid">
          <div>
            <label>Grado</label>
            <select value={gradeId} onChange={(e) => setGradeId(e.target.value)}>
              <option value="">Seleccione</option>
              {grades.map((g) => (
                <option key={g.id} value={g.id}>
                  {g.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label>Sección</label>
            <select
              value={sectionId}
              onChange={(e) => setSectionId(e.target.value)}
            >
              <option value="">Seleccione</option>
              {sections
                .filter((s) => String(s.grade_id) === String(gradeId))
                .map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.code || s.name}
                  </option>
                ))}
            </select>
          </div>
        </div>

        <div className="actions">
          <button
            className="btn btn-primary"
            onClick={generateRecord}
            disabled={loading}
          >
            {loading ? "Generando…" : "Generar Acta"}
          </button>
        </div>

        {recordId && (
          <div className="record-id">
            Academic Record ID: <strong>{recordId}</strong>
          </div>
        )}
      </div>

      {/* ESTADO DE FIRMAS */}
      <div className="panel">
        <h2>Estado de Firmas</h2>

        <div className="grid">
          <div>
            <label>Academic Record ID</label>
            <input
              type="number"
              value={recordId}
              onChange={(e) => setRecordId(e.target.value)}
              placeholder="Ej: 1"
            />
          </div>
        </div>

        <div className="actions">
          <button
            className="btn btn-secondary"
            onClick={checkStatus}
            disabled={loading}
          >
            {loading ? "Consultando…" : "Ver Estado"}
          </button>
        </div>

        {status && (
          <div className="status">
            <div>
              <span>Maestro Guía</span>
              <strong>
                {status.signed_roles?.includes("GUIDE_TEACHER")
                  ? "Firmado"
                  : "Pendiente"}
              </strong>
            </div>
            <div>
              <span>Coordinación</span>
              <strong>
                {status.signed_roles?.includes("COORDINATION")
                  ? "Firmado"
                  : "Pendiente"}
              </strong>
            </div>
            <div>
              <span>Dirección</span>
              <strong>
                {status.signed_roles?.includes("DIRECTOR")
                  ? "Firmado"
                  : "—"}
              </strong>
            </div>
            <div>
              <span>Acta completa</span>
              <strong>{status.is_fully_signed ? "Sí" : "No"}</strong>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}