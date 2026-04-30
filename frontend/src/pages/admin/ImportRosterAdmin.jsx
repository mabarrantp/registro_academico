import { useState } from "react";
import "./ImportRosterAdmin.css";

export default function ImportRosterAdmin() {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setMessage(null);
        setError(null);
    };

    const handleUpload = async () => {
        if (!file) {
            setError("Seleccione un archivo para importar");
            return;
        }

        try {
            setLoading(true);
            setError(null);
            setMessage(null);

            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch(
                `${import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"}/import/roster`,
                {
                    method: "POST",
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    },
                    body: formData,
                }
            );

            if (!response.ok) {
                throw new Error("Error al importar el padrón");
            }

            setMessage("Padrón importado correctamente");
            setFile(null);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="import-roster-admin">
            <h2>Importar Padrón de Estudiantes</h2>

            <div className="import-box">
                <input
                    type="file"
                    accept=".csv, .xlsx"
                    onChange={handleFileChange}
                />

                <button onClick={handleUpload} disabled={loading || !file}>
                    {loading ? "Importando..." : "Importar"}
                </button>
            </div>

            {message && <p className="success">{message}</p>}
            {error && <p className="error">{error}</p>}

            <div className="import-help">
                <p>
                    El archivo debe contener los datos de los estudiantes
                    en formato CSV o Excel.
                </p>
            </div>
        </div>
    );
}
``