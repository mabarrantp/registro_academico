import { useEffect, useMemo, useState } from "react";
import { api } from "../../services/api";
import "./QuarterWeightsAdmin.css";

const CATEGORIES = ["PROJECT", "CLASS_WORK", "HOMEWORK", "QUIZZES", "TEST"];

export default function QuarterWeightsAdmin() {
  const ctx = useMemo(() => ({ academicYear: 2025 }), []);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  const [quarters, setQuarters] = useState([]);
  const [sections, setSections] = useState([]);
  const [subjects, setSubjects] = useState([]);

  const [quarterId, setQuarterId] = useState("");
  const [sectionId, setSectionId] = useState("");
  const [subjectId, setSubjectId] = useState("");

  const [weights, setWeights] = useState(
    CATEGORIES.reduce((acc, c) => ({ ...acc, [c]: 0 }), {})
  );

  const total = CATEGORIES.reduce((sum, c) => sum + Number(weights[c] || 0), 0);

  useEffect(() => {
    loadCatalogs();
    // eslint-disable-next-line
  }, []);

  async function loadCatalogs() {
    setLoading(true);
    setMessage("");

    try {
      const [qRes, sRes, subRes] = await Promise.all([
        api.get("/quarters"),
        api.get("/sections"),
        api.get("/subjects"),
      ]);

      setQuarters(
        (qRes.data || []).filter(
          (q) => !q.academic_year || q.academic_year === ctx.academicYear
        )
      );

      setSections(
        (sRes.data || []).filter(
          (s) => !s.academic_year || s.academic_year === ctx.academicYear
        )
      );

      setSubjects(subRes.data || []);
    } catch (err) {
      console.error(err);
      setMessage("❌ Error cargando catálogos.");
    } finally {
      setLoading(false);
    }
  }

  async function loadWeights() {
    if (!quarterId || !sectionId || !subjectId) {
      setMessage("⚠️ Selecciona Quarter, Sección y Materia.");
      return;
    }

    try {
      const res = await api.get("/quarter-weights", {
        params: {
          quarter_id: quarterId,
          section_id: sectionId,
          subject_id: subjectId,
        },
      });

      if (!res.data || Object.keys(res.data).length === 0) {
        setWeights(CATEGORIES.reduce((a, c) => ({ ...a, [c]: 0 }), {}));
        setMessage("ℹ️ No hay ponderaciones guardadas.");
        return;
      }

      const pct = {};
      CATEGORIES.forEach((c) => {
        pct[c] = Math.round((res.data[c] || 0) * 100);
      });

      setWeights(pct);
      setMessage("✅ Ponderaciones cargadas.");
    } catch (err) {
      console.error(err);
      setMessage("❌ No se pudieron cargar ponderaciones.");
    }
  }

  async function saveWeights() {
    if (total !== 100) {
      setMessage(`⚠️ La suma debe ser 100%. Actual: ${total}%`);
      return;
    }

    setSaving(true);
    setMessage("");

    try {
      const payload = {};
      CATEGORIES.forEach((c) => {
        payload[c] = Number((weights[c] / 100).toFixed(4));
      });

      await api.post("/quarter-weights", {
        quarter_id: Number(quarterId),
        section_id: Number(sectionId),
        subject_id: Number(subjectId),
        weights: payload,
      });

      setMessage("✅ Ponderaciones guardadas correctamente.");
    } catch (err) {
      console.error(err);
      setMessage(
        err?.response?.data?.detail ||
          "❌ No se pudo guardar (¿quarter cerrado?)."
      );
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <div className="loading">Cargando ponderaciones…</div>;

  return (
    <div className="qw-admin">
      <h1>Ponderaciones por Quarter</h1>
      <p className="subtitle">
        Definición de pesos oficiales para el cálculo del quarter.
      </p>

      <div className="panel">
        <div className="grid">
          <div>
            <label>Quarter</label>
            <select value={quarterId} onChange={(e) => setQuarterId(e.target.value)}>
              <option value="">Seleccione</option>
              {quarters.map((q) => (
                <option key={q.id} value={q.id}>
                  {q.code || `Q${q.order}`} ({q.status})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label>Sección</label>
            <select value={sectionId} onChange={(e) => setSectionId(e.target.value)}>
              <option value="">Seleccione</option>
              {sections.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.code || s.name} (Grado {s.grade_id})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label>Materia</label>
            <select value={subjectId} onChange={(e) => setSubjectId(e.target.value)}>
              <option value="">Seleccione</option>
              {subjects.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="actions">
          <button className="btn btn-secondary" onClick={loadWeights}>
            Cargar
          </button>
        </div>

        {message && <div className="message">{message}</div>}
      </div>

      <div className="panel">
        <h2>Pesos (%)</h2>

        {CATEGORIES.map((c) => (
          <div className="weight-row" key={c}>
            <span>{c.replace("_", " ")}</span>
            <input
              type="number"
              min="0"
              max="100"
              value={weights[c]}
              onChange={(e) =>
                setWeights({ ...weights, [c]: Number(e.target.value) })
              }
            />
            <span>%</span>
          </div>
        ))}

        <div className={`total ${total === 100 ? "ok" : "bad"}`}>
          Total: {total}%
        </div>

        <div className="actions">
          <button
            className="btn btn-primary"
            onClick={saveWeights}
            disabled={saving}
          >
            {saving ? "Guardando…" : "Guardar"}
          </button>
        </div>
      </div>
    </div>
  );
}
