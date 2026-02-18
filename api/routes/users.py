from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from api.schemas import UserRegisterIn, UserOut, UserUpdateIn
from services.users import create_user_service, list_users_service, get_user_by_id_service, update_user_service, delete_user_service
from database.database import get_db
from helpers.log.logger import logger
from typing import Optional
from api.schemas import UsersPage, UserOut


router = APIRouter()
log = logger("users")


router = APIRouter()

@router.post("/register", summary="Registra um novo usuário", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegisterIn, db: Session = Depends(get_db)):
    try:
        user = create_user_service(
            db=db,
            name=payload.complete_name,
            email=payload.email,
            password=payload.password,
            roles=payload.roles or "user",
        )
        return user

    except ValueError as ve:
        detail = str(ve)
        if "cadastrado" in detail:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno ao registrar usuário.")


@router.get("/list-users", summary="Lista usuários com paginação, busca e filtros", response_model=UsersPage,)
def list_all_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Página atual (>=1)"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página (1-100)"),
    q: Optional[str] = Query(None, description="Busca por nome ou e-mail"),
    status: Optional[bool] = Query(None, description="Filtra por status (true/false)"),
    sort_by: str = Query("created_at", description="Campo para ordenação"),
    order: str = Query("desc", pattern="^(?i)(asc|desc)$", description="Ordem asc|desc"),
):
    items, total = list_users_service(
        db=db,
        page=page,
        page_size=page_size,
        q=q,
        status=status,
        sort_by=sort_by,
        order=order,
    )
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }



@router.get("/user/{user_id}", summary="Busca um usuário específico", response_model=UserOut)
def list_specific_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id_service(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    return user


@router.patch("/update/{user_id}", summary="Atualiza qualquer campo do usuário", response_model=UserOut)
def update_user(
    user_id: int,
    payload: UserUpdateIn,
    db: Session = Depends(get_db)
):
    try:
        user = update_user_service(
            db=db,
            user_id=user_id,
            complete_name=payload.complete_name,
            email=payload.email,
            password=payload.password,
            roles=payload.roles,
            status=payload.status
        )

    except ValueError as ve:
        detail = str(ve)
        if "cadastrado" in detail:
            raise HTTPException(status_code=409, detail=detail)
        raise HTTPException(status_code=400, detail=detail)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user


@router.delete("/delete/{user_id}", summary="Desativa um usuário")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = delete_user_service(db, user_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    return {"detail": "Usuário desativado com sucesso"}