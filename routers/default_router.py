from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse

from models.models import User, Poll, FilledPoll
from core.server import server

router = APIRouter()


@router.get("/")
def root(request: Request):
    addr = f"{request.client.host}:{request.client.port}"
    return {"Hello": "World", "addr": addr}


@router.post("game/fill/")
def fill_poll(filled_poll: FilledPoll):
    """
    :param filled_poll: a filled poll
    :return: a HTTP response
    """
    try:
        server.game.add_answer(filled_poll)
        return status.HTTP_200_OK
    except KeyError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


@router.get("game/lobby/")
def list_users():
    def json_generator():
        while True:
            yield jsonable_encoder(server.game.list_users())
    return StreamingResponse(json_generator(), media_type="application/x-ndjson")


@router.get("game/status/")
def list_users():
    json_compatible_item_data = jsonable_encoder(server.game.get_remaining_poll_targets())
    return JSONResponse(content=json_compatible_item_data)


@router.post("/register/")
def register(user: User):
    if server.game.register_user(user):
        return status.HTTP_200_OK
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="Username already taken"
    )


@router.post("/poll/{name}/save")
def save_poll(name: str, poll: Poll):
    server.save_poll(poll, name)


@router.get("/poll/{name}/load")
def load_poll(name: str) -> Poll:
    return server.load_poll(name)
