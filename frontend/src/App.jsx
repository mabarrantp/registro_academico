import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";

import AdminLayout from "./layouts/AdminLayout";
import GuideLayout from "./layouts/GuideLayout";
import RoleRoute from "./components/RoleRoute";

/* ===== ADMIN / COORDINATOR ===== */
import AdminHome from "./pages/admin/AdminHome";
import StudentsAdmin from "./pages/admin/StudentsAdmin";
import EnrollmentsAdmin from "./pages/admin/EnrollmentsAdmin";
import CoordinationDashboard from "./pages/admin/CoordinationDashboard";
import TeachersAtRisk from "./pages/admin/TeachersAtRisk";
import AuditLog from "./pages/admin/AuditLog";

/* ===== DOCENTE (COMPARTIDOS) ===== */
import GuideHome from "./pages/guide/GuideHome";
import GuideRisk from "./pages/guide/GuideRisk";
import GuideQuarterResults from "./pages/guide/GuideQuarterResults";

/* ===== ERRORES ===== */
import Error401 from "./pages/errors/Error401";
import Error403 from "./pages/errors/Error403";

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                {/* ========== LOGIN ========== */}
                <Route path="/login" element={<Login />} />

                {/* ========== ERRORES ========== */}
                <Route path="/401" element={<Error401 />} />
                <Route path="/403" element={<Error403 />} />

                {/* ========== ADMIN / COORDINATOR ========== */}
                <Route
                    path="/admin"
                    element={
                        <RoleRoute allowedRoles={["admin", "coordinator"]}>
                            <AdminLayout />
                        </RoleRoute>
                    }
                >
                    {/* Dashboard */}
                    <Route index element={<AdminHome />} />

                    {/* Administración */}
                    <Route path="students" element={<StudentsAdmin />} />
                    <Route path="enrollments" element={<EnrollmentsAdmin />} />

                    {/* Coordinación */}
                    <Route path="coordination" element={<CoordinationDashboard />} />
                    <Route path="teachers-at-risk" element={<TeachersAtRisk />} />

                    {/* Auditoría (solo Admin) */}
                    <Route path="audit" element={<AuditLog />} />

                    {/* ===== VISTAS DOCENTE PARA ADMIN ===== */}
                    <Route path="teacher" element={<GuideHome />} />
                    <Route path="teacher/risk" element={<GuideRisk />} />
                    <Route
                        path="teacher/quarter-results"
                        element={<GuideQuarterResults />}
                    />
                </Route>

                {/* ========== DOCENTE REAL ========== */}
                <Route
                    path="/guide"
                    element={
                        <RoleRoute allowedRoles={["teacher"]}>
                            <GuideLayout />
                        </RoleRoute>
                    }
                >
                    <Route index element={<GuideHome />} />
                    <Route path="risk" element={<GuideRisk />} />
                    <Route path="quarter-results" element={<GuideQuarterResults />} />
                </Route>

                {/* ========== ROOT ========== */}
                <Route path="/" element={<Navigate to="/login" replace />} />
                <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
        </BrowserRouter>
    );
}
