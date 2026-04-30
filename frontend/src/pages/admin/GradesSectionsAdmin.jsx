import { useEffect, useState } from "react";
import { getGrades, getSections } from "../../services/api";
import "./GradesSectionsAdmin.css";

function GradesSectionsAdmin() {
    const [grades, setGrades] = useState([]);
    const [sections, setSections] = useState([]);
    const [sectionId, setSectionId] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function loadSections() {
            try {
                const data = await getSections();
                setSections(data);
            } catch (e) {
                setError(e.message);
            }
        }
        loadSections();
    }, []);

    useEffect(() => {
        async function fetchGrades() {
            if (!sectionId) return;
            try {
                setLoading(true);
                setError(null);
                const data = await getGrades({ sectionId });
                setGrades(data.grades);
            } catch (e) {
                setError(e.message);
            } finally {
                setLoading(false);
            }
        }
        fetchGrades();
    }, [sectionId]);

    return (
        <div className="grades-sections-admin">
            <h2>Notas por Sección</h2>

            <label>
                Sección:&nbsp;
                <select value={sectionId} onChange={(e) => setSectionId(e.target.value)}>
                    <option value="">Seleccione</option>
                    {sections.map((s) => (
                        <option key={s.id} value={s.id}>{s.label}</option>
                    ))}
                </select>
            </label>

            {loading && <p>Cargando...</p>}
            {error && <p className="error">{error}</p>}

            {!loading && grades.length > 0 && (
                <table className="grades-table">
                    <thead>
                        <tr>
                            <th>Estudiante</th><th>Grado</th><th>Asignatura</th>
                            <th>Quarter</th><th>Nota</th><th>Cualitativo</th>
                        </tr>
                    </thead>
                    <tbody>
                        {grades.map((g, i) => (
                            <tr key={i}>
                                <td>{g.student}</td>
                                <td>{g.grade}</td>
                                <td>{g.subject}</td>
                                <td>{g.quarter}</td>
                                <td>{g.quantitative ?? "-"}</td>
                                <td>{g.qualitative}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default GradesSectionsAdmin;