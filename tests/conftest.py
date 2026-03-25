import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.api.deps import get_db

# Cria um banco de dados SQLite na memória (não salva no HD, some ao fechar)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# engine = O motor do banco. O connect_args é frescura exigida pelo SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Essa função substitui o seu banco real pelo banco de teste
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Avisa o FastAPI para trocar a dependência do banco
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def test_db():
    # Cria todas as tabelas no banco de teste antes de começar
    Base.metadata.create_all(bind=engine)
    yield
    # Destrói o banco de teste no final (limpa a sujeira)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(test_db):
    # Entrega um cliente do FastAPI já com o banco falso configurado
    with TestClient(app) as c:
        yield c