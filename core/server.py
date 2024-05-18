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


server = Server()
