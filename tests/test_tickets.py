def test_create_ticket_authenticated(client):
    # 1. PREPARAR: Criar usuário e fazer login para pegar a "chave" (token)
    client.post("/users/", json={
        "email": "cliente1@fluxdesk.com", 
        "password": "senha", 
        "role": "cliente"
    })
    
    login_response = client.post("/auth/login", data={
        "username": "cliente1@fluxdesk.com", 
        "password": "senha"
    })
    
    # Extrai o token da resposta de login
    token = login_response.json()["access_token"]
    
    # Prepara a "credencial" que vai junto com a requisição
    headers = {"Authorization": f"Bearer {token}"}

    # Dados do chamado em si
    ticket_data = {
        "title": "Sistema lento",
        "description": "O sistema não carrega a página inicial.",
        "category": "Software",
        "priority": "Alta"
    }

    # 2. AGIR: Tenta criar o chamado passando os dados E o token no cabeçalho
    response = client.post("/tickets/", json=ticket_data, headers=headers)

    # 3. AFIRMAR: Verifica se o chamado foi criado certinho
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Sistema lento"
    assert data["status"] == "Aberto"  # Verifica se o sistema colocou o status padrão
    assert "id" in data

def test_cliente_nao_pode_alterar_status(client):
    # 1. PREPARAR: Vamos logar de novo com o cliente que criamos no teste anterior
    login_response = client.post("/auth/login", data={
        "username": "cliente1@fluxdesk.com", 
        "password": "senha"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Dados da "tentativa de invasão" (cliente tentando fechar o chamado)
    update_data = {
        "status": "Fechado"
    }

    # 2. AGIR: O cliente dispara um PATCH na rota que é exclusiva para técnicos
    # (Como o banco de teste reseta a cada rodada, o chamado que criamos ali em cima será o ID 1)
    response = client.patch("/tickets/1/assign", json=update_data, headers=headers)

    # 3. AFIRMAR: O sistema TEM que barrar. 403 é o código web para "Proibido / Forbidden"
    assert response.status_code == 403
    
    data = response.json()

    assert data["detail"] == "Operação não permitida para o seu perfil."

def test_list_tickets_with_filters(client):
    # 1. PREPARAR: Cadastra um técnico e faz login
    client.post("/users/", json={
        "email": "inspetor@fluxdesk.com", 
        "password": "senha", 
        "role": "tecnico"
    })
    token = client.post("/auth/login", data={
        "username": "inspetor@fluxdesk.com", 
        "password": "senha"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. PREPARAR: Cria 3 chamados com prioridades diferentes
    # Dois de prioridade "Alta"
    client.post("/tickets/", json={"title": "Erro 1", "description": "...", "category": "A", "priority": "Alta"}, headers=headers)
    client.post("/tickets/", json={"title": "Erro 2", "description": "...", "category": "A", "priority": "Alta"}, headers=headers)
    # Um de prioridade "Baixa"
    client.post("/tickets/", json={"title": "Erro 3", "description": "...", "category": "B", "priority": "Baixa"}, headers=headers)

    # 3. AGIR e AFIRMAR: Testa o filtro de Alta prioridade
    response_alta = client.get("/tickets/?priority=Alta", headers=headers)
    dados_alta = response_alta.json()
    
    assert response_alta.status_code == 200
    assert len(dados_alta) == 2  # Tem que trazer exatamente os 2 chamados de alta prioridade
    assert dados_alta[0]["priority"] == "Alta"

    # 4. AGIR e AFIRMAR: Testa o filtro de Baixa prioridade
    response_baixa = client.get("/tickets/?priority=Baixa", headers=headers)
    dados_baixa = response_baixa.json()
    
    assert len(dados_baixa) == 1  # Tem que trazer só 1
    assert dados_baixa[0]["priority"] == "Baixa"