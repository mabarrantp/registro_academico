import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { getUserRole } from "../utils/token";
import "./Login.css";

import hcaLogo from "../assets/hca-logo.svg";

const API_URL =
    import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        try {
            const formData = new FormData();
            formData.append("username", username);
            formData.append("password", password);

            const response = await axios.post(
                `${API_URL}/auth/login`,
                formData,
                { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
            );

            localStorage.setItem("token", response.data.access_token);

            // ✅ REDIRECCIÓN POR ROL
            const role = getUserRole();

            if (role === "admin") navigate("/admin");
            else if (role === "coordinator") navigate("/coordinator");
            else if (role === "teacher") navigate("/guide");
            else navigate("/login");
        } catch {
            setError("Usuario o contraseña incorrectos");
        }
    };

    return (
        <div className="login-wrap">
            <div className="login-card">
                <div className="login-header">
                    {hcaLogo}
                    <h1>Iniciar sesión</h1>
                    <p className="login-subtitle">Registro Académico</p>
                </div>

                <form onSubmit={handleSubmit}>
                    <label>Usuario</label>
                    <input value={username} onChange={(e) => setUsername(e.target.value)} />

                    <label>Contraseña</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    <button className="primary">Entrar</button>
                    {error && <div className="msg">{error}</div>}
                </form>
            </div>
        </div>
    );
}
