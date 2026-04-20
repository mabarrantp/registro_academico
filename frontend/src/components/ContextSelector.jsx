import { useEffect, useState } from "react";
import { getGrades, getSubjects, getQuarters } from "../api.js";

export default function ContextSelector({ onConfirm }) {
  const [grades, setGrades] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [quarters, setQuarters] = useState([]);
  const [error, setError] = useState(null);

  const [gradeId, setGradeId] = useState("");
  const [subjectId, setSubjectId] = useState("");
  const [quarterId, setQuarterId] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const g = await getGrades();
        const s = await getSubjects();
        const q = await getQuarters();
        setGrades(g);
        setSubjects(s);
        setQuarters(q);
      } catch (e) {
        setError(e.message);
      }
    }
    load();
  }, []);

  function confirm() {
    const grade = grades.find((x) => x.id === Number(gradeId));
    const subject = subjects.find((x) => x.id === Number(subjectId));
    const quarter = quarters.find((x) => x.id === Number(quarterId));

    if (!grade || !subject || !quarter) {
      setError("Selecciona grado, materia y quarter");
      return;
    }

    onConfirm({
      academicYear: 2025,
      grade,
      subject,
      quarter,
    });
  }

  return (
    <div>
      <h2>Seleccionar contexto</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <select value={gradeId} onChange={(e) => setGradeId(e.target.value)}>
        <option value="">Grado</option>
        {grades.map((g) => (
          <option key={g.id} value={g.id}>{g.name}</option>
        ))}
      </select>

      <select value={subjectId} onChange={(e) => setSubjectId(e.target.value)}>
        <option value="">Materia</option>
        {subjects.map((s) => (
          <option key={s.id} value={s.id}>{s.name}</option>
        ))}
      </select>

      <select value={quarterId} onChange={(e) => setQuarterId(e.target.value)}>
        <option value="">Quarter</option>
        {quarters.map((q) => (
          <option key={q.id} value={q.id}>
            {q.code} ({q.status})
          </option>
        ))}
      </select>

      <button onClick={confirm}>Confirmar</button>
    </div>
  );
}