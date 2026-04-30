import { getUserRole } from "../utils/token";
import { hasPermission } from "../utils/permissions";

export default function usePermission(permission) {
    const role = getUserRole();
    return hasPermission(role, permission);
}
