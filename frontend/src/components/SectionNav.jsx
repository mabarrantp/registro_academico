import FeedbackMessage from "./FeedbackMessage";

export default function SectionNav({ context, activeSection, onGo, onReset }) {
  if (!context) return null;

  const isClosed = context.quarter.status === "CLOSED";

  return (
    <div className="topbar">
      <div className="topbar-left">
        <div className="topbar-title">Contexto</div>
        <div className="topbar-meta">
          <span><strong>Año:</strong> {context.academicYear}</span>
          <span><strong>Grado:</strong> {context.grade.name}</span>
          <span><strong>Materia:</strong> {context.subject.name}</span>
          <span><strong>Quarter:</strong> {context.quarter.code} ({context.quarter.status})</span>
        </div>
      </div>

      <div className="topbar-right">
        <div className="nav-buttons">
          <button
            className={activeSection === "register" ? "nav-btn active" : "nav-btn"}
            onClick={() => onGo("register")}
          >
            Registro
          </button>

          <button
            className={activeSection === "preview" ? "nav-btn active" : "nav-btn"}
            onClick={() => onGo("preview")}
            disabled={isClosed}
            title={isClosed ? "Quarter cerrado" : ""}
          >
            Preview
          </button>

          <button
            className={activeSection === "report" ? "nav-btn active" : "nav-btn"}
            onClick={() => onGo("report")}
          >
            Boletín
          </button>

          <button className="nav-btn secondary" onClick={onReset}>
            Cambiar contexto
          </button>
        </div>

        {isClosed && (
          <div style={{ marginTop: ".5rem" }}>
            <FeedbackMessage
              type="warning"
              message="🔒 Quarter cerrado: registro y recálculo deshabilitados."
            />
          </div>
        )}
      </div>
    </div>
  );
}
