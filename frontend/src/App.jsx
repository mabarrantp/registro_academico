import { useEffect, useState } from "react";
import Login from "./components/Login.jsx";
import ContextSelector from "./components/ContextSelector.jsx";
import { clearSession, getRole } from "./api.js";

function App() {
  const [session, setSession] = useState(null); // { role }
  const [context, setContext] = useState(null);

  useEffect(() => {
    const role = getRole();
    if (role) setSession({ role });
  }, []);

  function logout() {
    clearSession();
    setSession(null);
    setContext(null);
  }

  if (!session) {
    return (
      <div className="container">
        <h1>Sistema Académico</h1>
        <Login onLoggedIn={setSession} />
      </div>
    );
  }

  return (
    <div className="container">
      <h1>Sistema Académico</h1>

      <div className="card">
        <strong>Sesión:</strong> {session.role}
        <button style={{ marginLeft: "1rem" }} onClick={logout}>
          Cerrar sesión
        </button>
      </div>

      {!context ? (
        <ContextSelector onConfirm={setContext} />
      ) : (
        <div className="card">
          <h2>Contexto seleccionado</h2>
          <p>Año: {context.academicYear}</p>
          <p>Grado: {context.grade.name}</p>
          <p>Materia: {context.subject.name}</p>
          <p>
            Quarter: {context.quarter.code} ({context.quarter.status})
          </p>

          <p style={{ opacity: 0.8 }}>
            ✅ Siguiente paso: aquí conectamos Registro / Preview / ReportCard ya que Vite
            esté estable.
          </p>
        </div>
      )}
    </div>
  );
}

export default App;