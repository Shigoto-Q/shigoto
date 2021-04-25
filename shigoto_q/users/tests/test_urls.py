def test_an_admin_view(admin_client):
    response = admin_client.get("/admin/")
    assert response.status_code == 200


def test_users_permissions(admin_client):
    response = admin_client.get("/auth/users/me/")
    assert response.status_code == 401
