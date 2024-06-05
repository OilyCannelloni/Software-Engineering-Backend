import unittest

from core.game import Game
from models.models import User


class TestRegisterUser(unittest.TestCase):
    def test_register(self):
        game = Game()
        user = User(name="oilymacaroni")

        status = game._register_user_local(user)

        self.assertTrue(status)
        self.assertTrue(user in game.user_data.keys())

    def test_remove(self):
        game = Game()
        user = User(name="oilymacaroni")
        game._register_user_local(user)

        status = game.remove_user(User(name="abc"))
        self.assertFalse(status)
        self.assertTrue(user in game.user_data.keys())

        status = game.remove_user(user)
        self.assertTrue(status)
        self.assertFalse(user in game.user_data.keys())

    def test_remove_by_name(self):
        game = Game()
        user = User(name="oilymacaroni")
        game._register_user_local(user)

        status = game.remove_user_by_name("abc")
        self.assertFalse(status)
        self.assertTrue(user in game.user_data.keys())

        status = game.remove_user_by_name("oilymacaroni")
        self.assertTrue(status)
        self.assertFalse(user in game.user_data.keys())
