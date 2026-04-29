import { NavLink, Outlet } from "react-router-dom";
import logoUrl from "../assets/hca-logo.svg";
import "./GuideLayout.css";

export default function GuideLayout() {
  const ctx = {
    academicYear: 2025,
    grade: "8°",
    section: "A",
    role: "Maestro Guía",
  };

  return (
    <div className="hca-layout">
      {/* SIDEBAR */}
      <aside className="hca-sidebar">
        {/* LOGO (centrado, sin texto al lado) */}
        <div className="hca-brand">
          <img className="hca-logo" src={logoUrl} alt="Hosanna Christian Academy Logo" />
          <div className="hca-brand-caption">Registro Académico</div>
        </div>

        {/* CONTEXTO */}
        <div className="hca-context">
          <div>
            <span>Año</span>
            <strong>{ctx.academicYear}</strong>
          </div>
          <div>
            <span>Grado</span>
            <strong>{ctx.grade}</strong>
          </div>
          <div>
            <span>Sección</span>
            <strong>{ctx.section}</strong>
          </div>
        </div>

        {/* MENÚ */}
        <nav className="hca-menu">
          <MenuItem to="/guide" end>Resumen</MenuItem>
          <MenuItem to="/guide/risk">Riesgo Académico</MenuItem>
          <MenuItem to="/guide/quarter-results">Resultados del Quarter</MenuItem>
          <MenuItem to="/guide/remedials">Reparaciones</MenuItem>
          <MenuItem to="/guide/promotion">Promoción</MenuItem>
          <MenuItem to="/guide/acta">Acta Académica</MenuItem>
        </nav>
      </aside>

      {/* MAIN */}
      <main className="hca-main">
        <header className="hca-header">
          <div className="hca-header-left">{ctx.role}</div>
          <div className="hca-header-right">Usuario conectado</div>
        </header>

        <section className="hca-content">
          <Outlet />
        </section>
      </main>
    </div>
  );
}

function MenuItem({ to, end, children }) {
  return (
    <NavLink
      to={to}
      end={end}
      className={({ isActive }) => `hca-menu-item ${isActive ? "active" : ""}`}
    >
      {children}
    </NavLink>
  );
}
