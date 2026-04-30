import { getUserRole } from "../utils/token";
import { hasPermission } from "../utils/permissions";

/**
 * Renderiza children SOLO si el usuario
 * tiene el permiso indicado
 */
export default function Can({ permission, children }) {
    const role = getUserRole();

    if (!hasPermission(role, permission)) {
        return null;
    }

    return children;
}