def test_create_user(client):
    # 1. PREPARAR
    user_data = {
        "email": "robo@fluxdesk.com",
        "password": "senha_super_segura",
        "role": "cliente"
    }

    # 2. AGIR
    response = client.post("/users/", json=user_data)

    # 3. AFIRMAR
    assert response.status_code == 200
    
    data = response.json()
    
    # Confere apenas o que realmente existe na sua API
    assert data["email"] == "robo@fluxdesk.com"
    assert data["role"] == "cliente"
    assert "id" in data