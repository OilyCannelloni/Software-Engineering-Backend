import unittest

from core.server import server
from models.models import User

FILE_PATH = "file.json"


class TestListUsers(unittest.TestCase):
    def test_poll_list_users(self):
        poll = server.load_poll(FILE_PATH)
        user1 = User(name="oilymacaroni")
        user2 = User(name="among us")

        server.game.register_user(user1)
        server.game.register_user(user2)

        users_list = server.game.list_users()
        self.assertEqual(len(users_list), 2)
        self.assertEqual(user1, users_list[0])
        self.assertEqual(user2, users_list[1])
        self.assertEqual(user1.name, users_list[0].name)

        server.game.start_polling_phase(poll)
