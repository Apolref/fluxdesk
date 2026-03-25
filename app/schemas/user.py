from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    # O campo 'name' foi removido daqui porque não existe mais no banco!

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    email: EmailStr
    role: str       # <-- Adicionado para o Swagger mostrar se ele é cliente, tecnico, etc.
    is_active: bool

    class Config:
        from_attributes = True
        # Se você estiver usando uma versão mais antiga do Pydantic, talvez precise ser: orm_mode = True