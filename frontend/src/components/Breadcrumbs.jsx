import { Link, useLocation } from "react-router-dom";
import "../styles/Breadcrumbs.css";

export default function Breadcrumbs() {
    const location = useLocation();
    const parts = location.pathname.split("/").filter(Boolean);

    return (
        <nav className="hca-breadcrumbs">
            <Link to="/">Inicio</Link>

            {parts.map((part, index) => {
                const path = "/" + parts.slice(0, index + 1).join("/");
                const label = formatLabel(part);

                return (
                    <span key={path}>
                        <span className="sep">/</span>
                        <Link to={path}>{label}</Link>
                    </span>
                );
            })}
        </nav>
    );
}

function formatLabel(text) {
    return text
        .replace(/-/g, " ")
        .replace(/\b\w/g, (l) => l.toUpperCase());
}
