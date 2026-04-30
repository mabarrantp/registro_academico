def test_full_year_closure_flow(client, db, admin_user):
    # 1. Crear y abrir ciclo
    year = client.post("/academic-years", json={
        "name": "2025",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31"
    }).json()

    client.post(f"/academic-years/{year['id']}/open")

    # 2. Importar alumnos
    response = client.post(
        "/students/import-xlsx",
        json=[
            {
                "id_externo": "A001",
                "nombres": "Juan",
                "apellidos": "Perez",
                "fecha_nacimiento": "2010-05-01",
                "documento_identidad": "123"
            }
        ]
    )
    assert response.status_code == 200

    # 3. No permitir cerrar ciclo con quarter activo
    q = db.execute("select id from quarters limit 1").first()
    client.post(f"/quarters/{q.id}/open")

    response = client.post(
        "/admin/closure/close-year",
        params={"user_id": admin_user.id}
    )
    assert response.status_code == 409

    # 4. Cerrar quarter
    client.post(f"/quarters/{q.id}/close")

    # 5. Cerrar ciclo
    response = client.post(
        "/admin/closure/close-year",
        params={"user_id": admin_user.id}
    )
    assert response.status_code == 200

    # 6. Clasificar
    response = client.post(
        "/admin/closure/classify",
        params={"user_id": admin_user.id}
    )
    assert response.status_code == 200

    # 7. Promover
    response = client.post(
        "/admin/closure/promote",
        params={
            "user_id": admin_user.id,
            "academic_year_id": year["id"]
        }
    )
    assert response.status_code == 200
