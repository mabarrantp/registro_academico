import { useEffect, useState } from "react";
import { getStudents, createAssessment } from "../api.js";

const CATEGORIES = [
  { id: 1, label: "Classwork" },
  { id: 2, label: "Quiz" },
  { id: 3, label: "Homework" },
  { id: 4, label: "Project" },
  { id: 5, label: "Test" },
];

export default function AssessmentRegister({ context }) {
  const [students, setStudents] = useState([]);
  const [categoryId, setCategoryId] = useState("");
  const [assignmentName, setAssignmentName] = useState("");
  const [assignmentDate, setAssignmentDate] = useState("");
  const [scores, setScores] = useState({});
  const [msg, setMsg] = useState(null);
  const [loading, setLoading] = useState(false);

  const isClosed = context.quarter.status === "CLOSED";

  useEffect(() => {
    getStudents()
      .then(setStudents)
      .catch((e) => setMsg({ type: "error", text: e.message }));
  }, []);

  // ✅ FIX CRÍTICO AQUÍ
  function handleScoreChange(studentId, value) {
    setScores((prev) => ({
      ...prev,
      [studentId]: value,
    }));
  }

  async function saveActivity() {
    if (isClosed) {
      setMsg({ type: "error", text: "🔒 Quarter cerrado." });
      return;
    }

    if (!categoryId || !assignmentName || !assignmentDate) {
      setMsg({
        type: "error",
        text: "Debes indicar categoría, nombre y fecha del Assignment.",
      });
      return;
    }

    const studentsWithScore = students.filter(
      (s) => scores[s.id] !== undefined && scores[s.id] !== ""
    );

    if (studentsWithScore.length === 0) {
      setMsg({
        type: "error",
        text: "Debes ingresar al menos una nota.",
      });
      return;
    }

    setLoading(true);
    setMsg(null);

    try {
      for (const s of studentsWithScore) {
        await createAssessment({
          student_id: Number(s.id),
          subject_id: Number(context.subject.id),
          teacher_id: 1,
          grade_id: Number(context.grade.id),
          quarter_id: Number(context.quarter.id),
          category_id: Number(categoryId),
          score: Number(scores[s.id]),
          on_time: true,
          comments: `Assignment: ${assignmentName} | Date: ${assignmentDate}`,
        });
      }

      setScores({});
      setCategoryId("");
      setAssignmentName("");
      setAssignmentDate("");

      setMsg({
        type: "success",
        text: `✅ Assignment "${assignmentName}" registrado correctamente.`,
      });
    } catch (e) {
      setMsg({
        type: "error",
        text: e.message || "Error al guardar",
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
      <h2>Registro de Actividades</h2>

      {msg && <div className={`feedback ${msg.type}`}>{msg.text}</div>}

      <label>Categoría</label>
      <select
        value={categoryId}
        disabled={isClosed}
        onChange={(e) => setCategoryId(e.target.value)}
      >
        <option value="">Seleccione</option>
        {CATEGORIES.map((c) => (
          <option key={c.id} value={c.id}>{c.label}</option>
        ))}
      </select>

      <label>Assignment</label>
      <input
        type="text"
        value={assignmentName}
        disabled={isClosed}
        onChange={(e) => setAssignmentName(e.target.value)}
      />

      <label>Date Assigned</label>
      <input
        type="date"
        value={assignmentDate}
        disabled={isClosed}
        onChange={(e) => setAssignmentDate(e.target.value)}
      />

      <h3>Notas por alumno</h3>

      {students.map((s) => (
        <div key={s.id} style={{ marginBottom: "0.5rem" }}>
          {s.first_name} {s.last_name}
          <input
            type="number"
            min="0"
            max="100"
            disabled={isClosed}
            value={scores[s.id] ?? ""}
            onChange={(e) =>
              handleScoreChange(s.id, e.target.value)
            }
            style={{ marginLeft: "1rem", width: "100px" }}
          />
        </div>
      ))}

      <button onClick={saveActivity} disabled={loading || isClosed}>
        {loading ? "Guardando..." : "Guardar actividad"}
      </button>
    </div>
  );
}
