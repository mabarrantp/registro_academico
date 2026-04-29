import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";

// Layouts
import GuideLayout from "./layouts/GuideLayout";
import AdminLayout from "./layouts/AdminLayout";

// Guide pages
import GuideHome from "./pages/guide/GuideHome";
import GuideRisk from "./pages/guide/GuideRisk";
import GuideQuarterResults from "./pages/guide/GuideQuarterResults";
import GuideRemedials from "./pages/guide/GuideRemedials";
import GuidePromotion from "./pages/guide/GuidePromotion";
import GuideActa from "./pages/guide/GuideActa";

// Admin pages
import AdminHome from "./pages/admin/AdminHome";
import StudentsAdmin from "./pages/admin/StudentsAdmin";
import EnrollmentsAdmin from "./pages/admin/EnrollmentsAdmin";
import QuartersAdmin from "./pages/admin/QuartersAdmin";
import QuarterWeightsAdmin from "./pages/admin/QuarterWeightsAdmin";
import AcademicRecordsAdmin from "./pages/admin/AcademicRecordsAdmin";
import PromotionAdmin from "./pages/admin/PromotionAdmin";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />

        {/* Maestro Guía */}
        <Route
          path="/guide"
          element={
            <ProtectedRoute>
              <GuideLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<GuideHome />} />
          <Route path="risk" element={<GuideRisk />} />
          <Route path="quarter-results" element={<GuideQuarterResults />} />
          <Route path="remedials" element={<GuideRemedials />} />
          <Route path="promotion" element={<GuidePromotion />} />
          <Route path="acta" element={<GuideActa />} />
        </Route>

        {/* Admin */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <AdminLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<AdminHome />} />
          <Route path="students" element={<StudentsAdmin />} />
          <Route path="enrollments" element={<EnrollmentsAdmin />} />
          <Route path="quarters" element={<QuartersAdmin />} />
          <Route path="quarter-weights" element={<QuarterWeightsAdmin />} />
          <Route path="academic-records" element={<AcademicRecordsAdmin />} />
          <Route path="promotion" element={<PromotionAdmin />} />
        </Route>

        <Route path="*" element={<div style={{ padding: 20 }}>404</div>} />
      </Routes>
    </BrowserRouter>
  );
}