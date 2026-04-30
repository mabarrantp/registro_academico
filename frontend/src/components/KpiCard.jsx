export default function KpiCard({ title, value, subtitle }) {
    return (
        <div
            style={{
                background: "#ffffff",
                borderRadius: "12px",
                padding: "20px",
                minWidth: "200px",
                boxShadow: "0 4px 8px rgba(0,0,0,0.06)",
            }}
        >
            <h4 style={{ margin: 0, color: "#6b7280" }}>{title}</h4>
            <h2 style={{ margin: "8px 0", color: "#111827" }}>{value}</h2>
            {subtitle && (
                <p style={{ margin: 0, color: "#9ca3af", fontSize: "14px" }}>
                    {subtitle}
                </p>
            )}
        </div>
    );
}
