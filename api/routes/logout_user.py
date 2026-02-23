from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from helpers.log.logger import logger
from database.models.users import Users
from helpers.users.get_user import get_current_user


router = APIRouter()
log = logger("users")


@router.post("", summary="Logout user")
def logout_user(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter(Users.id == current_user["sub"]).first()

    user.refresh_token = None
    db.commit()

    return {"message": "Successfully logout user"}