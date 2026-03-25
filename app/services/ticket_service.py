from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate

def create_ticket(db: Session, ticket: TicketCreate, user_id: int):
    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        category=ticket.category,
        priority=ticket.priority,
        creator_id=user_id  # O ID vem do token do usuário logado
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

from typing import List # Adicione este import no topo se não tiver

def get_tickets(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    status: str = None, 
    creator_id: int = None
):
    query = db.query(Ticket)
    
    # Se passarmos um status (ex: "Aberto"), ele filtra
    if status:
        query = query.filter(Ticket.status == status)
    
    # Se passarmos um creator_id, ele mostra só os chamados daquela pessoa
    if creator_id:
        query = query.filter(Ticket.creator_id == creator_id)
        
    return query.offset(skip).limit(limit).all()

def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def update_ticket_status(db: Session, db_ticket: Ticket, status: str, assignee_id: int = None):
    db_ticket.status = status
    if assignee_id:
        db_ticket.assignee_id = assignee_id
    
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def delete_ticket(db: Session, db_ticket: Ticket):
    db.delete(db_ticket)
    db.commit()
    return True

from sqlalchemy import func

def get_ticket_stats(db: Session):
    # O comando correto é group_by (sem o 'code')
    stats = db.query(Ticket.status, func.count(Ticket.id)).group_by(Ticket.status).all()
    return {status: count for status, count in stats}