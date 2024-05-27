from fastapi import APIRouter, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from models.models import User, Poll, FilledPoll
from core.server import server

router = APIRouter()


@router.get("/")
def root(request: Request):
    addr = f"{request.client.host}:{request.client.port}"
    return {"Hello": "World", "addr": addr}


@router.post("/game/fill/")
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


@router.get("/game/lobby/")
def list_users():
    def json_generator():
        while True:
            yield jsonable_encoder(server.game.list_users())
    return StreamingResponse(json_generator(), media_type="application/x-ndjson")


@router.get("/game/status/")
def list_users():
    json_compatible_item_data = jsonable_encoder(server.game.list_users())
    return JSONResponse(content=json_compatible_item_data)


@router.get("/register/{name}")
def register(name: str, request: Request) -> StreamingResponse:
    register_result = server.game.register_user(User(name=name), request)
    if register_result is not False:
        return StreamingResponse(register_result, media_type="text/event-stream")
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Username already taken")


@router.post("/start-game")
def start_polling():
    server.game.start_game()
    return status.HTTP_200_OK


@router.post("/end-game")
def end_polling():
    server.game.end_game()
    return status.HTTP_200_OK


@router.post("/poll/{name}/save")
def save_poll(name: str, poll: Poll):
    server.save_poll(poll, name)


@router.get("/poll/{name}/load")
def load_poll(name: str) -> Poll:
    return server.load_poll(name)
