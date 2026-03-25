def test_login_success(client):
    # 1. PREPARAR: Criamos um usuário primeiro (porque o banco de teste começa vazio)
    client.post("/users/", json={
        "email": "tecnico@fluxdesk.com", 
        "password": "senha_segura", 
        "role": "tecnico"
    })

    # Dados para o login (Lembra que o OAuth2 usa 'username' em vez de 'email')
    login_data = {
        "username": "tecnico@fluxdesk.com",
        "password": "senha_segura"
    }

    # 2. AGIR: Dispara o POST pra rota de login. 
    # Nota importante: Login usa 'data=' (Formulário) e não 'json='!
    response = client.post("/auth/login", data=login_data)

    # 3. AFIRMAR: Confere se deu 200 e se o token veio na resposta
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    # Tenta logar com senha errada pra ver se o sistema bloqueia
    login_data = {
        "username": "tecnico@fluxdesk.com",
        "password": "senha_errada"
    }
    response = client.post("/auth/login", data=login_data)
    
    # 401 é o código padrão da web para "Não Autorizado"
    assert response.status_code == 401