from fastapi import APIRouter, HTTPException, status
from models.models import User
from core.server import game

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/register/")
def register(user: User):
    if game.register_user(user):
        return status.HTTP_200_OK
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Username already taken"
    )
