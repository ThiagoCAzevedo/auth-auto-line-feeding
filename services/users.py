from typing import Optional, Tuple, List
from sqlalchemy import or_, desc, asc, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models.users import Users
from helpers.users.validators import validate_password, validate_email_domain


def create_user_service(db: Session, name: str, email: str, password: str, roles: str = "user") -> Users:
    ok, msg = validate_email_domain(email)
    if not ok:
        raise ValueError(msg)

    existing = db.query(Users).filter(Users.email == email).first()
    if existing:
        raise ValueError("E-mail já cadastrado.")

    ok, msg = validate_password(password)
    if not ok:
        raise ValueError(msg)

    user = Users(
        complete_name=name,
        email=email,
        roles=roles or "user",
        status=True
    )
    user.set_password(password)

    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise ValueError("E-mail já cadastrado.")

    return user


def list_users_service(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    q: Optional[str] = None,
    status: Optional[bool] = None,
    sort_by: str = "created_at",  # ou 'complete_name', 'email', 'status'
    order: str = "desc",          # 'asc' ou 'desc'
) -> Tuple[List[Users], int]:
    """
    Retorna (lista_de_usuarios, total) respeitando filtros, busca, ordenação e paginação.
    """

    # Base query
    query = db.query(Users)

    # Filtro por status (True/False)
    if status is not None:
        query = query.filter(Users.status == status)

    # Busca simples em nome e e-mail
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(Users.complete_name.ilike(like), Users.email.ilike(like))
        )

    # Ordenação segura
    sort_columns = {
        "created_at": Users.created_at,
        "updated_at": Users.updated_at,
        "complete_name": Users.complete_name,
        "email": Users.email,
        "status": Users.status,
        "id": Users.id,
    }
    sort_col = sort_columns.get(sort_by, Users.created_at)
    sort_func = desc if order.lower() == "desc" else asc
    query = query.order_by(sort_func(sort_col))

    # Total antes da paginação
    total = query.count()

    # Paginação
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    offset = (page - 1) * page_size

    items = query.offset(offset).limit(page_size).all()

    return items, total



def get_user_by_id_service(db: Session, user_id: int) -> Users:
    user = db.query(Users).filter(Users.id == user_id).first()
    return user


def update_user_service(
    db: Session,
    user_id: int,
    complete_name: str | None = None,
    email: str | None = None,
    password: str | None = None,
    roles: str | None = None,
    status: bool | None = None
):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        return None

    # Atualizar nome
    if complete_name is not None:
        user.complete_name = complete_name

    # Atualizar e-mail (com validação de domínio + unicidade)
    if email is not None:
        ok, msg = validate_email_domain(email)
        if not ok:
            raise ValueError(msg)

        # Verificar se não existe outro usuário com este e-mail
        existing = (
            db.query(Users)
            .filter(and_(Users.email == email, Users.id != user_id))
            .first()
        )
        if existing:
            raise ValueError("E-mail já cadastrado por outro usuário.")

        user.email = email

    # Atualizar senha (com validação + hashing)
    if password is not None:
        ok, msg = validate_password(password)
        if not ok:
            raise ValueError(msg)

        user.set_password(password)

    # Atualizar roles
    if roles is not None:
        user.roles = roles

    # Atualizar status
    if status is not None:
        user.status = status

    db.commit()
    db.refresh(user)

    return user


def delete_user_service(db: Session, user_id: int) -> bool:
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        return False

    user.status = False  # soft delete
    db.commit()
    return True