from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import relationship

class TicketCreate(BaseModel):
    title: str
    description: str
    category: str
    priority: str = "Média"

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    priority: str
    status: str
    creator_id: int
    assignee_id: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}
        
comments = relationship("Comment", back_populates="ticket")

class TicketUpdate(BaseModel):
    status: Optional[str] = None

class TicketDashboard(BaseModel):
    total: int
    abertos: int
    em_atendimento: int
    fechados: int