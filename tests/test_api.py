from fastapi.testclient import TestClient
from app.main import app

# Cria um "cliente falso" que consegue fazer requisições pra nossa API sem precisar ligar o servidor de verdade
client = TestClient(app)

def test_api_is_running():
    # O robô tenta acessar a rota da documentação
    response = client.get("/docs")
    
    # A gente "afirma" (assert) que o status tem que ser 200
    assert response.status_code == 200