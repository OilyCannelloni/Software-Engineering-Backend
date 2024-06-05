import json

from fastapi import APIRouter, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import StreamingResponse, JSONResponse

from models.models import User, Poll, FilledPoll
import core.server

router = APIRouter()
server = core.server.Server()

@router.get("/")
def root(request: Request):
    addr = f"{request.client.host}:{request.client.port}"
    return {"Hello": "World", "addr": addr}


@router.post("/game/fill")
def fill_poll(filled_poll: FilledPoll):
    """
    :param filled_poll: a filled poll
    :return: a HTTP response
    """
    try:
        server.game.add_answer(filled_poll)
        return status.HTTP_200_OK
    except KeyError:
        return status.HTTP_400_BAD_REQUEST


@router.post("/poll/set")
def fill_poll(poll: Poll):
    """
    :param poll: A poll to set
    :return: a HTTP response
    """
    server.game.poll = Poll


@router.get("/game/lobby")
async def list_users(request: Request):
    result = server.game.stream_users(request)
    if result is not None:
        return StreamingResponse(result, media_type="text/event-stream")
    raise HTTPException(500)


@router.get("/game/{user}/status")
async def list_remaining_users(user: str):
    json_compatible_item_data = json.dumps(
        server.game.get_remaining_poll_targets(user=User(name=user))
    )
    return JSONResponse(content=json_compatible_item_data)


@router.get("/game/{user}/polls")
async def list_answers_about(username: str):
    json_compatible_item_data = json.dumps(
        server.game.get_answers_about(user=User(name=username)),
        default=lambda obj: obj.__dict__, indent=4
    )
    return JSONResponse(content=json_compatible_item_data)


@router.get("/game/{user}/polls")
async def list_answers_about(username: str):
    json_compatible_item_data = json.dumps(
        server.game.get_answers_about(user=User(name=username)),
        default=lambda obj: obj.__dict__, indent=4
    )
    return JSONResponse(content=json_compatible_item_data)


@router.get("/register/{name}")
async def register(name: str, request: Request) -> StreamingResponse:
    register_result = server.game.register_user(User(name=name), request)
    if register_result is not False:
        return StreamingResponse(register_result, media_type="text/event-stream")
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="Username already taken"
    )


@router.post("/remove/{name}")
def remove_user_by_name(name: str):
    if server.game.remove_user_by_name(name):
        return status.HTTP_200_OK
    return status.HTTP_304_NOT_MODIFIED


@router.post("/game/start")
def start_polling():
    server.game.start_game()
    return status.HTTP_200_OK


@router.post("/game/end")
def end_polling():
    server.game.end_game()
    return status.HTTP_200_OK


@router.post("/poll/{name}/save")
def save_poll(name: str, poll: Poll):
    server.save_poll(poll, name)


@router.get("/poll/{name}/load")
def load_poll(name: str) -> Poll:
    return server.load_poll(name)
