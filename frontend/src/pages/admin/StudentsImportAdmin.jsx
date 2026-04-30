import { useState } from "react";
import "./StudentsImportAdmin.css";

export default function StudentsImportAdmin() {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setMessage(null);
        setError(null);
    };

    const handleImport = async () => {
        if (!file) {
            setError("Seleccione un archivo para importar estudiantes");
            return;
        }

        try {
            setLoading(true);
            setError(null);
            setMessage(null);

            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch(
                `${import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"}/import/students`,
                {
                    method: "POST",
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    },
                    body: formData,
                }
            );

            if (!response.ok) {
                throw new Error("Error al importar estudiantes");
            }

            setMessage("Estudiantes importados correctamente");
            setFile(null);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="students-import-admin">
            <h2>Importar Estudiantes</h2>

            <div className="import-box">
                <input
                    type="file"
                    accept=".csv, .xlsx"
                    onChange={handleFileChange}
                />

                <button onClick={handleImport} disabled={!file || loading}>
                    {loading ? "Importando..." : "Importar"}
                </button>
            </div>

            {message && <p className="success">{message}</p>}
            {error && <p className="error">{error}</p>}

            <div className="import-help">
                <p>
                    El archivo debe contener los datos de los estudiantes en
                    formato CSV o Excel.
                </p>
            </div>
        </div>
    );
}