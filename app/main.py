from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Novo import
from app.db.session import engine
from app.db.base import Base
from app.api.routes.users import router as users_router
from app.api.routes.auth import router as auth_router
from app.api.routes.tickets import router as tickets_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FluxDesk API", description="Sistema de Chamados Técnicos")

# --- Configuração do CORS ---
# Em desenvolvimento, usamos ["*"] para permitir qualquer origem (porta).
# Em produção, você trocaria o "*" pelo domínio real do seu site (ex: "https://meu-fluxdesk.com.br")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Lista VIP
    allow_credentials=True,
    allow_methods=["*"], # Permite GET, POST, PUT, DELETE
    allow_headers=["*"], # Permite todos os cabeçalhos (incluindo o nosso Token JWT)
)
# ----------------------------

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(tickets_router, prefix="/tickets", tags=["Tickets"])