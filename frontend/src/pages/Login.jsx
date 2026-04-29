import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import logoUrl from "../assets/hca-logo.svg";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin123");
  const [showPass, setShowPass] = useState(false);
  const [remember, setRemember] = useState(true);

  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  async function handleLogin(e) {
    e.preventDefault();
    setMsg("");
    setLoading(true);

    try {
      // ✅ backend directo (evita 404 en 5173)
      const res = await axios.post("http://127.0.0.1:8000/auth/login", null, {
        params: { username, password },
      });

      const token = res.data?.access_token || res.data?.token;

      if (!token) {
        console.log("Respuesta login:", res.data);
        setMsg("❌ No se recibió token del backend.");
        return;
      }

      if (remember) localStorage.setItem("access_token", token);
      else sessionStorage.setItem("access_token", token);

      // ✅ decide adónde mandar después
      navigate("/guide"); // cambia a "/admin" si prefieres
    } catch (err) {
      console.error(err);
      setMsg(err?.response?.data?.detail || "❌ Usuario o contraseña incorrectos.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-wrap">
      <div className="login-card">
        <div className="login-header">
          <img className="login-logo" src={logoUrl} alt="Hosanna Christian Academy" />
          <div>
            <h1>Iniciar sesión</h1>
            <p className="muted">Sistema de Registro Académico</p>
          </div>
        </div>

        <form onSubmit={handleLogin}>
          <label>Usuario</label>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="usuario"
            autoComplete="username"
          />

          <label>Contraseña</label>
          <div className="pass-row">
            <input
              type={showPass ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="contraseña"
              autoComplete="current-password"
            />
            <button
              type="button"
              className="ghost"
              onClick={() => setShowPass((v) => !v)}
            >
              {showPass ? "Ocultar" : "Ver"}
            </button>
          </div>

          <div className="login-options">
            <label className="check">
              <input
                type="checkbox"
                checked={remember}
                onChange={(e) => setRemember(e.target.checked)}
              />
              Recordarme
            </label>

            <span className="help">¿Olvidaste tu contraseña?</span>
          </div>

          <button className="primary" type="submit" disabled={loading}>
            {loading ? "Ingresando…" : "Entrar"}
          </button>
        </form>

        {msg && <div className="msg">{msg}</div>}

        <div className="login-footer">
          <span className="muted small">
            © {new Date().getFullYear()} Hosanna Christian Academy
          </span>
        </div>
      </div>
    </div>
  );
}
