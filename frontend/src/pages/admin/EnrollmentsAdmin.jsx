import { useEffect, useState } from "react";
import { api } from "../../services/api";
import "./EnrollmentsAdmin.css";

export default function EnrollmentsAdmin() {
  const [studentCode, setStudentCode] = useState("");
  const [gradeId, setGradeId] = useState("");
  const [sectionId, setSectionId] = useState("");
  const [academicYear] = useState(2025);

  const [grades, setGrades] = useState([]);
  const [sections, setSections] = useState([]);

  const [message, setMessage] = useState("");

  useEffect(() => {
    api.get("/grades").then((res) => setGrades(res.data || []));
    api.get("/sections").then((res) => setSections(res.data || []));
  }, []);

  async function createEnrollment() {
    setMessage("");

    try {
      await api.post("/enrollments", {
        student_code: studentCode,
        grade_id: Number(gradeId),
        section_id: Number(sectionId),
        academic_year: academicYear,
      });

      setMessage("✅ Matrícula registrada correctamente.");
      setStudentCode("");
      setGradeId("");
      setSectionId("");
    } catch (err) {
      console.error(err);
      setMessage(
        err?.response?.data?.detail || "❌ No se pudo registrar la matrícula."
      );
    }
  }

  return (
    <div className="panel">
      <h2>Matrícula</h2>

      <div className="grid">
        <div>
          <label>Código del Estudiante</label>
          <input
            placeholder="2025-02-0001"
            value={studentCode}
            onChange={(e) => setStudentCode(e.target.value)}
          />
        </div>

        <div>
          <label>Grado</label>
          <select value={gradeId} onChange={(e) => setGradeId(e.target.value)}>
            <option value="">Seleccione</option>
            {grades.map((g) => (
              <option key={g.id} value={g.id}>
                {g.label}
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
                  {s.code}
                </option>
              ))}
          </select>
        </div>

        <div>
          <label>Año académico</label>
          <input type="number" value={academicYear} disabled />
        </div>
      </div>

      <div className="actions">
        <button className="btn btn-primary" onClick={createEnrollment}>
          Matricular
        </button>
      </div>

      {message && <div className="message">{message}</div>}
    </div>
  );
}