import { useEffect, useState } from "react";
import { api } from "../../services/api";
import "./StudentsAdmin.css";

export default function StudentsAdmin() {
  const [grades, setGrades] = useState([]);

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [entryYear] = useState(2025);
  const [entryGradeId, setEntryGradeId] = useState("");

  const [message, setMessage] = useState("");
  const [createdStudent, setCreatedStudent] = useState(null);

  useEffect(() => {
    api.get("/grades").then((res) => setGrades(res.data || []));
  }, []);

  async function createStudent() {
    setMessage("");
    setCreatedStudent(null);

    try {
      const res = await api.post("/students", {
        first_name: firstName,
        last_name: lastName,
        entry_year: entryYear,
        entry_grade_id: Number(entryGradeId),
      });

      setCreatedStudent(res.data);
      setMessage("✅ Estudiante creado correctamente.");

      setFirstName("");
      setLastName("");
      setEntryGradeId("");
    } catch (err) {
      console.error(err);
      setMessage(
        err?.response?.data?.detail || "❌ No se pudo crear el estudiante."
      );
    }
  }

  return (
    <div className="panel">
      <h2>Nuevo Estudiante</h2>

      <div className="grid">
        <div>
          <label>Nombres</label>
          <input value={firstName} onChange={(e) => setFirstName(e.target.value)} />
        </div>

        <div>
          <label>Apellidos</label>
          <input value={lastName} onChange={(e) => setLastName(e.target.value)} />
        </div>

        <div>
          <label>Año de ingreso</label>
          <input type="number" value={entryYear} disabled />
        </div>

        <div>
          <label>Grado de ingreso</label>
          <select value={entryGradeId} onChange={(e) => setEntryGradeId(e.target.value)}>
            <option value="">Seleccione</option>
            {grades.map((g) => (
              <option key={g.id} value={g.id}>
                {g.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="actions">
        <button className="btn btn-primary" onClick={createStudent}>
          Guardar Estudiante
        </button>
      </div>

      {message && <div className="message">{message}</div>}

      {createdStudent && (
        <div className="message">
          <strong>Código asignado:</strong>{" "}
          {createdStudent.student_code}
        </div>
      )}
    </div>
  );
}
