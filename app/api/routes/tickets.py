from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate, TicketDashboard
from app.services import ticket_service
from app.api.deps import get_current_user, RoleChecker
from app.models.user import User
from app.schemas.comment import CommentCreate
from app.api import deps
from app.models.user import User
from typing import Optional

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
    status: Optional[str] = None,
    priority: Optional[str] = None, # Nosso filtro novo
    mine: bool = False, # O seu filtro original mantido!
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Trava de Segurança Nível Banco: 
    # Cliente SEMPRE tem o creator_id travado no ID dele, não importa o que ele digite no Swagger.
    if current_user.role == "cliente":
        creator_id = current_user.id
    else:
        # Se for Técnico ou Admin, ele vê tudo (None), a não ser que ele marque a caixinha "mine=True"
        creator_id = current_user.id if mine else None

    # Chamamos o Service passando todos os filtros possíveis
    tickets = ticket_service.get_tickets(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        priority=priority,
        creator_id=creator_id
    )
    
    return tickets

@router.get("/dashboard", response_model=TicketDashboard)
def read_dashboard(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Retorna as métricas gerais do sistema (Total de chamados, abertos, etc).
    """
    # Proteção: Clientes comuns não podem ver os números gerais da empresa
    if current_user.role == "cliente":
        raise HTTPException(
            status_code=403, 
            detail="Operação não permitida para o seu perfil."
        )
    
    # Chama o nosso serviço que faz a contagem direto no banco de dados
    return ticket_service.get_dashboard_metrics(db=db)

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