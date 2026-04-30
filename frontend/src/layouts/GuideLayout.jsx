import { NavLink, Outlet } from "react-router-dom";
import Header from "../components/Header";
import "./GuideLayout.css";
import logoUrl from "../assets/hca-logo.svg";

export default function GuideLayout() {
    const ctx = {
        academicYear: 2025,
        grade: "8°",
        section: "A",
    };

    return (
        <div className="hca-layout">
            <aside className="hca-sidebar">
                <div className="hca-brand">
                    {logoUrl}
                    <div className="hca-brand-caption">
                        Registro Académico
                    </div>
                </div>

                <div className="hca-context">
                    <div><span>Año</span><strong>{ctx.academicYear}</strong></div>
                    <div><span>Grado</span><strong>{ctx.grade}</strong></div>
                    <div><span>Sección</span><strong>{ctx.section}</strong></div>
                </div>

                <nav className="hca-menu">
                    <MenuItem to="/guide" end>Resumen</MenuItem>
                    <MenuItem to="/guide/risk">Riesgo Académico</MenuItem>
                    <MenuItem to="/guide/quarter-results">Resultados</MenuItem>
                    <MenuItem to="/guide/remedials">Reforzamiento</MenuItem>
                    <MenuItem to="/guide/promotion">Promoción</MenuItem>
                    <MenuItem to="/guide/acta">Acta Académica</MenuItem>
                </nav>
            </aside>

            <section className="hca-main">
                <Header title="Panel del Maestro Guía" />

                <div className="hca-content">
                    <Outlet />
                </div>
            </section>
        </div>
    );
}

function MenuItem({ to, end, children }) {
    return (
        <NavLink
            to={to}
            end={end}
            className={({ isActive }) =>
                `hca-menu-item ${isActive ? "active" : ""}`
            }
        >
            {children}
        </NavLink>
    );
}