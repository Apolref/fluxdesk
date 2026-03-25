from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FluxDesk"
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgrespassword@localhost:5432/fluxdesk_db"
    
    # Novas variáveis para o JWT
    SECRET_KEY: str = "chave_secreta_super_segura_para_o_fluxdesk_123" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()