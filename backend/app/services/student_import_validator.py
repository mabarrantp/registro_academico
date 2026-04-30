from datetime import date

REQUIRED_COLUMNS = {
    "id_externo",
    "nombres",
    "apellidos",
    "fecha_nacimiento",
    "documento_identidad",
}


def validate_student_import_row(row: dict):
    missing = REQUIRED_COLUMNS - set(row.keys())
    if missing:
        return f"Missing columns: {', '.join(missing)}"

    if not row["nombres"].strip():
        return "First name is required"

    if not row["apellidos"].strip():
        return "Last name is required"

    try:
        birth = date.fromisoformat(str(row["fecha_nacimiento"]))
        if birth > date.today():
            return "Birth date cannot be in the future"
    except Exception:
        return "Invalid birth date format (YYYY-MM-DD)"

    return None

