import { NavLink, Outlet } from "react-router-dom";
import logoUrl from "../assets/hca-logo.svg";
import "./AdminLayout.css";

export default function AdminLayout() {
  const ctx = {
    academicYear: 2025,
    role: "Registro Académico (Admin)",
  };

  function logout() {
    localStorage.removeItem("access_token");
    sessionStorage.removeItem("access_token");
    window.location.href = "/login";
  }

  return (
    <div className="hca-layout">
      <aside className="hca-sidebar">
        <div className="hca-brand">
          {logoUrl}
          <div className="hca-brand-caption">Registro Académico</div>
        </div>

        <div className="hca-context">
          <div><span>Año</span><strong>{ctx.academicYear}</strong></div>
          <div><span>Rol</span><strong>Admin</strong></div>
        </div>

        <nav className="hca-menu">
          <MenuItem to="/admin" end>Dashboard</MenuItem>
          <MenuItem to="/admin/students">Estudiantes</MenuItem>
          <MenuItem to="/admin/enrollments">Matrículas</MenuItem>
          <MenuItem to="/admin/quarters">Quarters</MenuItem>
          <MenuItem to="/admin/quarter-weights">Ponderaciones</MenuItem>
          <MenuItem to="/admin/academic-records">Actas</MenuItem>
          <MenuItem to="/admin/promotion">Promoción</MenuItem>
        </nav>
      </aside>

      <main className="hca-main">
        <header className="hca-header">
          <div className="hca-header-left">{ctx.role}</div>
          <div className="hca-header-right">
            <span className="hca-user">Usuario conectado</span>
            {/* ✅ Botón estándar */}
            <button className="btn btn-outline" onClick={logout}>
              Cerrar sesión
            </button>
          </div>
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