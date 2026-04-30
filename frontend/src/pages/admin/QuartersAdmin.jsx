import { useEffect, useState } from "react";
import { getAcademicYears } from "../../services/api";
import "./QuartersAdmin.css";

export default function QuartersAdmin() {
    const [years, setYears] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchAcademicYears() {
            try {
                setLoading(true);
                setError(null);

                const data = await getAcademicYears();
                setYears(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchAcademicYears();
    }, []);

    return (
        <div className="quarters-admin">
            <h2>Años Académicos / Quarters</h2>

            {loading && <p>Cargando información...</p>}

            {error && <p className="error">{error}</p>}

            {!loading && !error && years.length === 0 && (
                <p>No hay años académicos registrados.</p>
            )}

            {!loading && !error && years.length > 0 && (
                <table className="quarters-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Año Académico</th>
                        </tr>
                    </thead>
                    <tbody>
                        {years.map((y) => (
                            <tr key={y.id}>
                                <td>{y.id}</td>
                                <td>{y.year}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
