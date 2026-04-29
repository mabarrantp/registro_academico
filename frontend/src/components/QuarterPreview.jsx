import { useState } from "react";
import { calculateQuarterGrade } from "../api.js";

export default function QuarterPreview({ context }) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState(null);

  async function handleCalculate() {
    setLoading(true);
    setMsg(null);

    try {
      const data = await calculateQuarterGrade({
        student_id: 1, // ✅ temporal (luego lo hacemos por estudiante)
        subject_id: context.subject.id,
        grade_id: context.grade.id,
        quarter_id: context.quarter.id,
      });

      setResult(data);
    } catch (e) {
      setMsg({ type: "error", text: e.message });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h2>Vista previa del Quarter</h2>

      <p>
        <strong>Quarter:</strong> {context.quarter.code} (
        {context.quarter.status})
      </p>

      <button onClick={handleCalculate} disabled={loading}>
        {loading ? "Calculando..." : "Calcular nota del Quarter"}
      </button>

      {msg && <div className={`feedback ${msg.type}`}>{msg.text}</div>}

      {result && (
        <div className="feedback success" style={{ marginTop: "1rem" }}>
          ✅ Nota final del Quarter:{" "}
          <strong>{Number(result.final_score).toFixed(2)}</strong>
        </div>
      )}
    </div>
  );
}
