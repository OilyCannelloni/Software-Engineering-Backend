import os
from typing import List
import socket

from core.game import Game
from models.models import Poll
from fastapi import HTTPException, status


class Server:
    pool_save_path = __file__[:__file__.find("Software-Engineering-Backend") + len(
        "Software-Engineering-Backend")] + "/data/pools/"

    def __init__(self):
        self.game = Game()

    @staticmethod
    def __no_dir_in_path(filename: str) -> bool:
        if os.path.dirname(filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Poll name cannot contain directories",
            )
        return True

    @staticmethod
    def save_poll(poll: Poll, filename: str) -> bool:
        os.makedirs(os.path.dirname(Server.pool_save_path), exist_ok=True)
        Server.__no_dir_in_path(filename)
        full_filename = f"{Server.pool_save_path}{filename}"
        with open(full_filename, "w") as file:
            file.write(poll.to_json())
            return True

    @staticmethod
    def load_poll(filename: str) -> Poll:
        Server.__no_dir_in_path(filename)
        full_filename = f"{Server.pool_save_path}{filename}"
        with open(full_filename, "r") as file:
            content = file.read()
            return Poll.from_json(content)

    @staticmethod
    def get_all_pools() -> List[str]:
        return os.listdir(Server.pool_save_path)

    @staticmethod
    def remove_pool(filename: str) -> None:
        Server.__no_dir_in_path(filename)
        full_filename = f"{Server.pool_save_path}{filename}"
        if os.path.exists(full_filename):
            os.remove(full_filename)
    @staticmethod
    def get_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            return f"Error: {e}"


# server = Server()
