import unittest

from core.server import Server
from models.models import User

FILE_PATH = "file.json"


class TestCaseCommonSetUpTwoUsersStartGame(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.server = Server()
        poll = cls.server.load_poll(FILE_PATH)
        cls.user1 = User(name="oilymacaroni")
        cls.user2 = User(name="among us")
        cls.server.game._register_user_local(cls.user1)
        cls.server.game._register_user_local(cls.user2)
        cls.server.game.set_poll(poll)
        cls.server.game.start_game()
