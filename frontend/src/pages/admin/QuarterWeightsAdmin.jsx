import { useEffect, useState } from "react";
import { getAcademicYears } from "../../services/api";
import "./QuarterWeightsAdmin.css";
export default function QuarterWeigthsAdmin() {
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
        <div className="quarter-weights-admin">
            <h2>Pesos de Quarters</h2>

            {loading && <p>Cargando configuración...</p>}
            {error && <p className="error">{error}</p>}

            {!loading && !error && years.length === 0 && (
                <p>No hay años académicos configurados.</p>
            )}

            {!loading && !error && years.length > 0 && (
                <table className="quarter-weights-table">
                    <thead>
                        <tr>
                            <th>ID Año</th>
                            <th>Año Académico</th>
                            <th>Peso Q1</th>
                            <th>Peso Q2</th>
                            <th>Peso Q3</th>
                            <th>Peso Q4</th>
                        </tr>
                    </thead>
                    <tbody>
                        {years.map((y) => (
                            <tr key={y.id}>
                                <td>{y.id}</td>
                                <td>{y.year}</td>
                                {/* 
                  En producción, estos pesos provendrán del backend.
                  Aquí se muestran valores por defecto/placeholder
                  sin refactorizar ni inventar endpoints.
                */}
                                <td>25%</td>
                                <td>25%</td>
                                <td>25%</td>
                                <td>25%</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
