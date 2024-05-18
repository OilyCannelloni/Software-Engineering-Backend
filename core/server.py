from game import Game
from models.models import Poll


class Server:
    def __init__(self):
        self.game = Game()

    @staticmethod
    def save_poll(poll: Poll, filename: str):
        with open(filename, "w") as file:
            file.write(poll.to_json())


server = Server()
