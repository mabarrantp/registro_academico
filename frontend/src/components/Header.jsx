import { useNavigate } from "react-router-dom";
import Breadcrumbs from "./Breadcrumbs";
import { getUserFromToken } from "../utils/token";
import "../styles/Header.css";

export default function Header({ title }) {
    const navigate = useNavigate();
    const user = getUserFromToken();

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login", { replace: true });
    };

    return (
        <header className="hca-header">
            <div className="hca-header-left">
                <div className="hca-header-title">{title}</div>
                <Breadcrumbs />
            </div>

            <div className="hca-header-right">
                <div className="hca-user-info">
                    <span className="hca-user-name">
                        {user?.name}
                    </span>
                    <span className="hca-user-role">
                        {user?.role}
                    </span>
                </div>

                <button
                    className="btn btn-outline hca-logout"
                    onClick={handleLogout}
                >
                    Salir
                </button>
            </div>
        </header>
    );
}
