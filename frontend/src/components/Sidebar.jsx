import { NavLink, Link } from "react-router-dom";
import { Role } from "../utils/token";
import "../styles/sidebar.css";
import logo from "../assets/hca-logo.svg";

export default function Sidebar() {
    const role = getUserRole();

    const isAdmin = role === "admin";
    const isCoordinator = role === "coordinator";
    const isTeacher = role === "teacher";

    const homeRoute = isTeacher ? "/guide" : "/admin";

    return (
        <aside className="sidebar">
            {/* HEADER / LOGO */}
            <div className="sidebar-header">
                <Link to={homeRoute} className="sidebar-logo-link">
                    <img src={logo} alt="Logo HCA" className="sidebar-logo" />
                </Link>

                <div className="sidebar-title">
                    <span>Registro Académico</span>
                    <small>Hosanna</small>
                </div>
            </div>

            <nav className="sidebar-nav">
                {/* ================= ADMINISTRACIÓN ================= */}
                {(isAdmin || isCoordinator) && (
                    <>
                        <div className="sidebar-section">Administración</div>

                        <NavLink to="/admin" end className="sidebar-link">
                            Dashboard
                        </NavLink>

                        <NavLink to="/admin/students" className="sidebar-link">
                            Estudiantes
                        </NavLink>

                        <NavLink to="/admin/enrollments" className="sidebar-link">
                            Matrículas
                        </NavLink>
                    </>
                )}

                {/* ================= COORDINACIÓN ================= */}
                {(isAdmin || isCoordinator) && (
                    <>
                        <div className="sidebar-section">Coordinación</div>

                        <NavLink to="/admin/coordination" className="sidebar-link">
                            Dashboard Coordinación
                        </NavLink>

                        <NavLink
                            to="/admin/teachers-at-risk"
                            className="sidebar-link"
                        >
                            Docentes en Riesgo
                        </NavLink>
                    </>
                )}

                {/* ================= DOCENTE ================= */}
                {(isAdmin || isCoordinator || isTeacher) && (
                    <>
                        <div className="sidebar-section">Docente</div>

                        <NavLink
                            to={isTeacher ? "/guide" : "/admin/teacher"}
                            end
                            className="sidebar-link"
                        >
                            Panel Docente
                        </NavLink>

                        <NavLink
                            to={isTeacher ? "/guide/risk" : "/admin/teacher/risk"}
                            className="sidebar-link"
                        >
                            Riesgo Académico
                        </NavLink>

                        <NavLink
                            to={
                                isTeacher
                                    ? "/guide/quarter-results"
                                    : "/admin/teacher/quarter-results"
                            }
                            className="sidebar-link"
                        >
                            Resultados
                        </NavLink>
                    </>
                )}

                {/* ================= SISTEMA ================= */}
                {isAdmin && (
                    <>
                        <div className="sidebar-section">Sistema</div>

                        <NavLink to="/admin/audit" className="sidebar-link">
                            Auditoría
                        </NavLink>
                    </>
                )}
            </nav>
        </aside>
    );
}

