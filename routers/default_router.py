from fastapi import APIRouter, HTTPException, status
from starlette.requests import Request

from models.models import User, Poll
from core.server import server

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
    if server.game.register_user(user):
        return status.HTTP_200_OK
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Username already taken"
    )


@router.post("/poll/{name}/save")
def save_poll(name: str, poll: Poll):
    server.save_poll(poll, name)


@router.get("/poll/{name}/load")
def load_poll(name: str) -> Poll:
    return server.load_poll(name)
