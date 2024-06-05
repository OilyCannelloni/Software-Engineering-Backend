import unittest

from core.server import Server
from models.models import User

FILE_PATH = "file.json"


class TestListUsers(unittest.TestCase):
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

    def test_poll_list_users(self):
        users_list = self.server.game.list_users()
        self.assertEqual(len(users_list), 2)
        self.assertEqual(self.user1, users_list[0])
        self.assertEqual(self.user2, users_list[1])
        self.assertEqual(self.user1.name, users_list[0].name)

