def test_products_url(admin_client):
    response = admin_client.get("/api/v1/products/")
    assert response.status_code == 200
