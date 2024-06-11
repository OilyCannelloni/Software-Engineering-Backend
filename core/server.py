import socket

from core.game import Game
from models.models import Poll


class Server:
    def __init__(self):
        self.game = Game()

    @staticmethod
    def save_poll(poll: Poll, filename: str) -> bool:
        with open(filename, "w") as file:
            file.write(poll.to_json())
            return True

    @staticmethod
    def load_poll(filename: str) -> Poll:
        with open(filename, "r") as file:
            content = file.read()
            return Poll.from_json(content)

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
