import { useEffect, useState } from "react";

// Componentes
import Login from "./components/Login.jsx";
import ContextSelector from "./components/ContextSelector.jsx";
import QuarterPreview from "./components/QuarterPreview.jsx";
import AssessmentRegister from "./components/AssessmentRegister.jsx";

// API helpers
import { getRole, clearSession } from "./api.js";

function App() {
  // ===============================
  // Estado de sesión y contexto
  // ===============================
  const [session, setSession] = useState(null);   // { role }
  const [context, setContext] = useState(null);   // contexto académico confirmado

  // ===============================
  // Restaurar sesión si existe token
  // ===============================
  useEffect(() => {
    const token = localStorage.getItem("token");
    const role = getRole();

    if (typeof token === "string" && token.length > 10 && role) {
      setSession({ role });
    }
  }, []);

  // ===============================
  // Cerrar sesión
  // ===============================
  function logout() {
    clearSession();
    setSession(null);
    setContext(null);
  }

  // ===============================
  // SIN sesión → Login
  // ===============================
  if (!session) {
    return (
      <div className="container">
        <h1>Sistema Académico</h1>
        <Login onLoggedIn={setSession} />
      </div>
    );
  }

  // ===============================
  // CON sesión → Flujo académico
  // ===============================
  return (
    <div className="container">
      <h1>Sistema Académico</h1>

      {/* =========================
          Información de sesión
         ========================= */}
      <div className="card">
        <strong>Sesión:</strong> {session.role}
        <button style={{ marginLeft: "1rem" }} onClick={logout}>
          Cerrar sesión
        </button>
      </div>

      {/* =========================
          Selección de contexto
         ========================= */}
      {!context ? (
        <ContextSelector onConfirm={setContext} />
      ) : (
        <>
          {/* =========================
              Resumen del contexto
             ========================= */}
          <div className="card">
            <h2>Contexto confirmado</h2>
            <p><strong>Año:</strong> {context.academicYear}</p>
            <p><strong>Grado:</strong> {context.grade.name}</p>
            <p><strong>Materia:</strong> {context.subject.name}</p>
            <p>
              <strong>Quarter:</strong>{" "}
              {context.quarter.code} ({context.quarter.status})
            </p>
          </div>

          {/* =========================
              Vista previa del Quarter
             ========================= */}
          <QuarterPreview context={context} />

          {/* =========================
              Registro de actividades
             ========================= */}
          <AssessmentRegister context={context} />
        </>
      )}
    </div>
  );
}

export default App;
