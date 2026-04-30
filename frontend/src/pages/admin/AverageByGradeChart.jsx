import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend,
} from "chart.js";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend
);

export default function AverageByGradeChart() {
    const [grades, setGrades] = useState([]);
    const [averages, setAverages] = useState([]);
    const [loading, setLoading] = useState(true);

    const API_URL =
        import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

    useEffect(() => {
        async function loadData() {
            const res = await fetch(
                `${API_URL}/dashboard/coordination/average-by-grade`,
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    },
                }
            );
            const data = await res.json();

            setGrades(data.map((d) => d.grade));
            setAverages(data.map((d) => d.average));
            setLoading(false);
        }

        loadData();
    }, []);

    if (loading) return <p>Cargando gráfico…</p>;

    return (
        <Bar
            data={{
                labels: grades,
                datasets: [
                    {
                        label: "Promedio",
                        data: averages,
                        backgroundColor: "#2D6EB4",
                    },
                ],
            }}
            options={{
                responsive: true,
                plugins: {
                    legend: { display: false },
                },
            }}
        />
    );
}
