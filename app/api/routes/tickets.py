from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from app.services import ticket_service
from app.api.deps import get_current_user, RoleChecker
from app.models.user import User
from app.schemas.comment import CommentCreate

from typing import List # Adicione este import no topo
from fastapi import APIRouter, Depends, HTTPException, status # Adicione HTTPException e status aqui
from app.schemas.comment import CommentCreate, CommentResponse
from app.services import comment_service

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
    ticket_update: TicketUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["tecnico", "admin"]))
):
    # Atualiza o ticket normalmente
    db_ticket = ticket_service.update_ticket(db, ticket_id=ticket_id, ticket_update=ticket_update)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    # --- A MÁGICA DO HISTÓRICO COMEÇA AQUI ---
    # Se o status foi alterado, cria um comentário automático
    if ticket_update.status:
        mensagem = f"⚠️ O status do chamado foi alterado para: {ticket_update.status} pelo técnico."
        comentario_automatico = CommentCreate(text=mensagem)
        
        comment_service.create_comment(
            db=db,
            comment=comentario_automatico,
            ticket_id=ticket_id,
            author_id=current_user.id
        )
    # -----------------------------------------

    return db_ticket

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

@router.post("/{ticket_id}/comments", response_model=CommentResponse)
def add_comment(
    ticket_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    # Qualquer usuário logado pode comentar (Cliente, Técnico ou Admin)
    current_user: User = Depends(get_current_user) 
):
    # Primeiro verifica se o ticket existe
    db_ticket = ticket_service.get_ticket_by_id(db, ticket_id=ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    # Cria o comentário passando o texto da requisição, o ID da URL e o ID do Token
    return comment_service.create_comment(
        db=db, 
        comment=comment, 
        ticket_id=ticket_id, 
        author_id=current_user.id
    )

@router.get("/{ticket_id}/comments", response_model=List[CommentResponse])
def get_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verifica se o ticket existe
    db_ticket = ticket_service.get_ticket_by_id(db, ticket_id=ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket não encontrado")
    
    return comment_service.get_comments_by_ticket(db=db, ticket_id=ticket_id)