from fastapi import APIRouter
from models.models import User

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/register/")
def register(user: User):
    return {"msg": f"Hello, {user.name}! You have been registered!"}
