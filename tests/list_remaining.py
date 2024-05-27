import unittest

from core.server import server
from models.models import User, FilledPoll, Answer, QuestionOption, QuestionTextbox

FILE_PATH = "file.json"


class TestListUsers(unittest.TestCase):
    def test_poll_list_remaining(self):
        poll = server.load_poll(FILE_PATH)
        user1 = User(name="oilymacaroni")
        user2 = User(name="among us")
        user3 = User(name="a")

        server.game.register_user(user1)
        server.game.register_user(user2)
        server.game.register_user(user3)

        answer1 = Answer(question_name="q1", value=[QuestionOption() for _ in range(2)])
        answer2 = Answer(question_name="q2", value=QuestionTextbox())
        filled_poll = FilledPoll(
            answers=[answer1, answer2], user_about=user1, user_filling=user2
        )

        server.game.start_polling_phase(poll)
        server.game.add_answer(filled_poll)

        users_list1 = server.game.get_remaining_poll_targets(user1)
        users_list2 = server.game.get_remaining_poll_targets(user2)
        users_list3 = server.game.get_remaining_poll_targets(user3)

        self.assertEqual(len(users_list1), 2)
        self.assertEqual(len(users_list2), 1)
        self.assertEqual(len(users_list3), 2)

        self.assertEqual(user2, users_list1[0])
        self.assertEqual(user3, users_list2[-1])

        server.game.start_polling_phase(poll)
