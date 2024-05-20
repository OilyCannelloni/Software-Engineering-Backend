from fastapi import APIRouter, HTTPException, status
from starlette.requests import Request

from models.models import User
from core.server import game

router = APIRouter()


@router.get("/")
def root(request: Request):
    addr = f"{request.client.host}:{request.client.port}"
    return {
        "Hello": "World",
        "addr": addr
    }


@router.post("/register/")
def register(user: User):
    if game.register_user(user):
        return status.HTTP_200_OK
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Username already taken"
    )
