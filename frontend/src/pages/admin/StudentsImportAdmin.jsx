import { useState } from "react";
import { api } from "../../services/api";
import "./StudentsImportAdmin.css";

export default function StudentsImportAdmin() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function importExcel() {
    if (!file) return;

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post("/students/import-xlsx", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setResult({
        created: 0,
        errors: ["❌ Error al importar el archivo"],
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="panel">
      <h2>Importación Masiva de Estudiantes (Excel)</h2>

      <input
        type="file"
        accept=".xlsx"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <div className="actions">
        <button className="btn btn-primary" onClick={importExcel} disabled={loading}>
          {loading ? "Importando…" : "Importar Excel"}
        </button>
      </div>

      {result && (
        <div className="result">
          <p>✅ Estudiantes creados: {result.created}</p>

          {result.errors.length > 0 && (
            <>
              <p>⚠️ Errores:</p>
              <ul>
                {result.errors.map((e, i) => (
                  <li key={i}>{e}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}
