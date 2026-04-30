import { Navigate } from "react-router-dom";
import { getUserRole } from "../utils/token";

export default function RoleRoute({ allowedRoles, children }) {
    const role = getUserRole();

    if (!role) {
        return <Navigate to="/401" replace />;
    }

    if (!allowedRoles.includes(role)) {
        return <Navigate to="/403" replace />;
    }

    return children;
}
