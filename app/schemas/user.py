from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import relationship

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

    model_config = {"from_attributes": True}


# Lembre-se de importar o relationship se não estiver lá: from sqlalchemy.orm import relationship
comments = relationship("Comment", back_populates="author")