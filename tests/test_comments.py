def test_create_and_read_comment(client):
    # 1. PREPARAR: Cria o usuário, loga e pega o token
    client.post("/users/", json={
        "email": "comentarista@fluxdesk.com", 
        "password": "senha", 
        "role": "tecnico"
    })
    token = client.post("/auth/login", data={
        "username": "comentarista@fluxdesk.com", "password": "senha"
    }).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. PREPARAR: Cria o chamado que vai receber o comentário
    ticket_response = client.post("/tickets/", json={
        "title": "Chamado para teste de comentário",
        "description": "Descrição do chamado",
        "category": "Dúvida",
        "priority": "Baixa"
    }, headers=headers)
    ticket_id = ticket_response.json()["id"]

    # 3. AGIR: O técnico envia um comentário nesse chamado
    comment_data = {"text": "Já estou analisando o seu problema!"}
    response_post = client.post(f"/tickets/{ticket_id}/comments", json=comment_data, headers=headers)
    
    # 4. AFIRMAR: Verifica se o POST deu certo
    assert response_post.status_code == 200
    assert response_post.json()["text"] == "Já estou analisando o seu problema!"

    # 5. AGIR DE NOVO: Vamos testar se a rota de LER os comentários também funciona
    response_get = client.get(f"/tickets/{ticket_id}/comments", headers=headers)
    
    # 6. AFIRMAR FINAL: A lista de comentários deve ter pelo menos 1 item
    assert response_get.status_code == 200
    comentarios = response_get.json()
    assert len(comentarios) >= 1
    assert comentarios[0]["text"] == "Já estou analisando o seu problema!"