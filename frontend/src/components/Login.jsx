import { useState } from "react";
import { login, setSession } from "../api.js";

export default function Login({ onLoggedIn }) {
  const [username, setUsername] = useState("teacher1");
  const [password, setPassword] = useState("1234");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleLogin() {
    setLoading(true);
    setError(null);

    try {
      const res = await login(username, password);
      setSession(res.access_token, res.role);
      onLoggedIn({ role: res.role });
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">
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
        {loading ? "Entrando..." : "Entrar"}
      </button>

      {error && <div className="feedback error">❌ {error}</div>}
    </div>
  );
}
