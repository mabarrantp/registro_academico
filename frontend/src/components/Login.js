import { useState } from "react";
import { login } from "../api";

export default function Login({ onLoggedIn }) {
  const [username, setUsername] = useState("teacher1");
  const [password, setPassword] = useState("1234");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState(null);

  async function handleLogin() {
    setLoading(true);
    setMsg(null);

    try {
      const res = await login(username, password);

      // Guardar token y rol
      localStorage.setItem("token", res.access_token); // ✅ solo token, sin "Bearer"
      localStorage.setItem("role", res.role);

      setMsg({ type: "success", text: "✅ Login correcto" });
      onLoggedIn({ role: res.role });
    } catch (e) {
      setMsg({ type: "error", text: `❌ ${e.message}` });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card" style={{ maxWidth: 420, margin: "0 auto" }}>
      <h2>Iniciar sesión</h2>

      <label>Usuario</label>
      <input value={username} onChange={(e) => setUsername(e.target.value)} />

      <label>Contraseña</label>
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleLogin} disabled={loading}>
        {loading ? "Ingresando..." : "Entrar"}
      </button>

      {msg && (
        <div
          className="feedback"
          style={{
            marginTop: "1rem",
            padding: "0.75rem",
            borderRadius: "6px",
            border: msg.type === "success" ? "1px solid #16a34a" : "1px solid #dc2626",
            background: msg.type === "success" ? "#052e16" : "#450a0a",
            color: msg.type === "success" ? "#bbf7d0" : "#fecaca",
          }}
        >
          {msg.text}
        </div>
      )}
    </div>
  );
}