import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../services/api";
import "./AdminHome.css";

export default function AdminHome() {
  const ctx = useMemo(() => ({ academicYear: 2025 }), []);

  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState([]);

  const [studentsCount, setStudentsCount] = useState(null);
  const [teachersCount, setTeachersCount] = useState(null);
  const [enrollmentsCount, setEnrollmentsCount] = useState(null);
  const [sectionsCount, setSectionsCount] = useState(null);

  const [quartersOpen, setQuartersOpen] = useState(null);
  const [quartersClosed, setQuartersClosed] = useState(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setErrors([]);

      const reqs = [
        api.get("/students", { params: { academic_year: ctx.academicYear } }),
        api.get("/teachers"),
        api.get("/enrollments"),
        api.get("/sections"),
        api.get("/quarters"),
      ];

      const res = await Promise.allSettled(reqs);

      const pushErr = (name, reason) => {
        setErrors((prev) => [...prev, `${name}: ${reason?.message || "Error"}`]);
      };

      // Students
      if (res[0].status === "fulfilled") {
        const data = res[0].value.data;
        setStudentsCount(Array.isArray(data) ? data.length : null);
      } else {
        setStudentsCount(null);
        pushErr("Students", res[0].reason);
      }

      // Teachers
      if (res[1].status === "fulfilled") {
        const data = res[1].value.data;
        setTeachersCount(Array.isArray(data) ? data.length : null);
      } else {
        setTeachersCount(null);
        pushErr("Teachers", res[1].reason);
      }

      // Enrollments
      if (res[2].status === "fulfilled") {
        const data = res[2].value.data;
        if (Array.isArray(data)) {
          const filtered = data.filter((e) =>
            e?.academic_year ? e.academic_year === ctx.academicYear : true
          );
          setEnrollmentsCount(filtered.length);
        } else setEnrollmentsCount(null);
      } else {
        setEnrollmentsCount(null);
        pushErr("Enrollments", res[2].reason);
      }

      // Sections
      if (res[3].status === "fulfilled") {
        const data = res[3].value.data;
        if (Array.isArray(data)) {
          const filtered = data.filter((s) =>
            s?.academic_year ? s.academic_year === ctx.academicYear : true
          );
          setSectionsCount(filtered.length);
        } else setSectionsCount(null);
      } else {
        setSectionsCount(null);
        pushErr("Sections", res[3].reason);
      }

      // Quarters
      if (res[4].status === "fulfilled") {
        const data = res[4].value.data;
        if (Array.isArray(data)) {
          const yearFiltered = data.filter((q) =>
            q?.academic_year ? q.academic_year === ctx.academicYear : true
          );
          setQuartersOpen(yearFiltered.filter((q) => String(q.status).toUpperCase() === "OPEN").length);
          setQuartersClosed(yearFiltered.filter((q) => String(q.status).toUpperCase() === "CLOSED").length);
        } else {
          setQuartersOpen(null);
          setQuartersClosed(null);
        }
      } else {
        setQuartersOpen(null);
        setQuartersClosed(null);
        pushErr("Quarters", res[4].reason);
      }

      setLoading(false);
    }

    load();
  }, [ctx]);

  return (
    <div className="ah-wrap">
      <div className="ah-head">
        <h1>Dashboard</h1>
        <div className="ah-sub">Año académico {ctx.academicYear}</div>
      </div>

      {loading ? (
        <div className="ah-loading">Cargando indicadores…</div>
      ) : (
        <>
          <div className="ah-cards">
            <KpiCard label="Estudiantes" value={studentsCount} tone="blue" />
            <KpiCard label="Profesores" value={teachersCount} tone="blue2" />
            <KpiCard label="Matrículas (año)" value={enrollmentsCount} tone="green" />
            <KpiCard label="Secciones (año)" value={sectionsCount} tone="blue" />
            <KpiCard label="Quarters abiertos" value={quartersOpen} tone="orange" />
            <KpiCard label="Quarters cerrados" value={quartersClosed} tone="red" />
          </div>

          {errors.length > 0 && (
            <div className="ah-warn">
              <div className="ah-warn-title">Avisos</div>
              <ul>
                {errors.map((e, i) => (
                  <li key={i}>{e}</li>
                ))}
              </ul>
              <div className="ah-warn-foot">
                * Si un endpoint aún no existe o requiere permisos, el dashboard mostrará N/A.
              </div>
            </div>
          )}

          <div className="ah-panel">
            <h2>Acciones rápidas</h2>

            <div className="ah-actions">
              <QuickLink to="/admin/students" title="Estudiantes" desc="Listado y filtros." />
              <QuickLink to="/admin/enrollments" title="Matrículas" desc="Matrícula tardía y listados." />
              <QuickLink to="/admin/quarters" title="Quarters" desc="Abrir / cerrar Q1–Q4." />
              <QuickLink to="/admin/quarter-weights" title="Ponderaciones" desc="Pesos por quarter." />
              <QuickLink to="/admin/academic-records" title="Actas" desc="Generar y revisar firmas." />
              <QuickLink to="/admin/promotion" title="Promoción" desc="Ejecutar cierre anual." />
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function KpiCard({ label, value, tone }) {
  const safe = value === null || value === undefined ? "N/A" : value;

  return (
    <div className={`ah-card ${tone || ""}`}>
      <div className="ah-card-value">{safe}</div>
      <div className="ah-card-label">{label}</div>
    </div>
  );
}

function QuickLink({ to, title, desc }) {
  return (
    <Link to={to} className="ah-link">
      <div className="ah-link-title">{title}</div>
      <div className="ah-link-desc">{desc}</div>
    </Link>
  );
}