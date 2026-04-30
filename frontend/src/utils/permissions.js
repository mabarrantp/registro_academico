/**
 * Mapa central de permisos por rol
 * Este archivo define QUÉ puede hacer cada rol
 */

export const PERMISSIONS = {
    admin: [
        "view",
        "create",
        "edit",
        "delete",
        "import",
        "export",
    ],

    coordinator: [
        "view",
        "create",
        "edit",
        "export",
    ],

    teacher: [
        "view",
    ],
};

/**
 * Verifica si un rol tiene un permiso
 */
export function hasPermission(role, permission) {
    if (!role) return false;
    return PERMISSIONS[role]?.includes(permission) ?? false;
}