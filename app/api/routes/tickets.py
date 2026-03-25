from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.ticket import TicketCreate, TicketResponse
from app.services import ticket_service
from app.api.deps import get_current_user, RoleChecker
from app.models.user import User

from typing import List # Adicione este import no topo
from fastapi import APIRouter, Depends, HTTPException, status # Adicione HTTPException e status aqui

# Cria uma regra que só deixa passar quem for técnico ou admin
allow_tech_admin = RoleChecker(["tecnico", "admin"])

router = APIRouter()

@router.post("/", response_model=TicketResponse)
def create_new_ticket(
    ticket: TicketCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Exige login
):
    return ticket_service.create_ticket(db=db, ticket=ticket, user_id=current_user.id)


@router.get("/", response_model=List[TicketResponse])
def read_tickets(
    skip: int = 0, 
    limit: int = 100, 
    status: str = None, # Novo parâmetro opcional
    mine: bool = False, # Novo parâmetro para ver "só os meus"
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    creator_id = current_user.id if mine else None
    
    tickets = ticket_service.get_tickets(
        db, 
        skip=skip, 
        limit=limit, 
        status=status, 
        creator_id=creator_id
    )
    return tickets

@router.patch("/{ticket_id}/assign", response_model=TicketResponse)
def assign_ticket(
    ticket_id: int, 
    db: Session = Depends(get_db),
    # OLHA A MÁGICA AQUI:
    current_user: User = Depends(allow_tech_admin) 
):
    db_ticket = ticket_service.get_ticket_by_id(db, ticket_id=ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    return ticket_service.update_ticket_status(db, db_ticket, "Em Atendimento", current_user.id)

@router.patch("/{ticket_id}/close", response_model=TicketResponse)
def close_ticket(
    ticket_id: int, 
    db: Session = Depends(get_db),
    # OLHA A MÁGICA AQUI DE NOVO:
    current_user: User = Depends(allow_tech_admin)
):
    db_ticket = ticket_service.get_ticket_by_id(db, ticket_id=ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    if db_ticket.assignee_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas o técnico atribuído pode finalizar")
    return ticket_service.update_ticket_status(db, db_ticket, "Finalizado")

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_ticket = ticket_service.get_ticket_by_id(db, ticket_id=ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    # SEGURANÇA: Verifica se quem está tentando deletar é o dono
    if db_ticket.creator_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Você não tem permissão para deletar um chamado que não é seu"
        )
    
    ticket_service.delete_ticket(db=db, db_ticket=db_ticket)
    return None

@router.get("/stats/summary")
def get_tickets_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ticket_service.get_ticket_stats(db)