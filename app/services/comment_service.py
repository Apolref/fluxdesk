from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

def create_comment(db: Session, comment: CommentCreate, ticket_id: int, author_id: int):
    # Monta o comentário juntando o texto do usuário com os IDs que pegamos da rota/token
    db_comment = Comment(
        text=comment.text,
        ticket_id=ticket_id,
        author_id=author_id
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    return db_comment

def get_comments_by_ticket(db: Session, ticket_id: int):
    # Busca todos os comentários que pertencem a um ticket específico
    return db.query(Comment).filter(Comment.ticket_id == ticket_id).all()