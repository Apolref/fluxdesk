from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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

    class Config:
        from_attributes = True