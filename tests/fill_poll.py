import unittest

from fastapi.exceptions import ValidationException

from core.server import server
from models.models import User, Answer, QuestionTextbox, QuestionOption, FilledPoll

FILE_PATH = "file.json"


class TestFillPoll(unittest.TestCase):
    def test_fill_poll(self):
        poll = server.load_poll(FILE_PATH)
        user1 = User(name="oilymacaroni")
        user2 = User(name="among us")

        server.game.register_user(user1)
        server.game.register_user(user2)

        server.game.start_polling_phase(poll)

        answer1 = Answer(question_name="q1", value=[QuestionOption() for _ in range(2)])
        answer2 = Answer(question_name="q2", value=QuestionTextbox())
        filled_poll = FilledPoll(
            answers=[answer1, answer2], user_about=user1, user_filling=user2
        )

        validation = server.game.validate_answers(filled_poll)
        result = server.game.add_answer(filled_poll)
        self.assertTrue(validation is None)
        self.assertTrue(result)
        self.assertTrue(server.game.user_data[user2][user1] is not None)
        self.assertTrue(len(server.game.user_data[user2][user1]) == 2)

    def test_fill_poll_bad_time(self):
        user1 = User(name="oilymacaroni")
        user2 = User(name="among us")

        server.game.register_user(user1)
        server.game.register_user(user2)

        answer1 = Answer(question_name="q1", value=[QuestionOption() for _ in range(2)])
        answer2 = Answer(question_name="q2", value=QuestionTextbox())
        filled_poll = FilledPoll(
            answers=[answer1, answer2], user_about=user1, user_filling=user2
        )
        errors = []
        try:
            validation = server.game.validate_answers(filled_poll)
        except AttributeError as e:
            errors.append(e)
        self.assertTrue(len(errors) == 1)
        self.assertTrue(type(errors[0]) == AttributeError)

    def test_fill_poll_bad_answer(self):
        poll = server.load_poll(FILE_PATH)
        user1 = User(name="oilymacaroni")
        user2 = User(name="among us")

        server.game.register_user(user1)
        server.game.register_user(user2)

        server.game.start_polling_phase(poll)

        answer1 = Answer(question_name="q2", value=[QuestionOption() for _ in range(2)])
        answer2 = Answer(question_name="q1", value=QuestionTextbox())
        filled_poll = FilledPoll(
            answers=[answer1, answer2], user_about=user1, user_filling=user2
        )
        errors = []
        try:
            server.game.validate_answers(filled_poll)
        except ValueError as e:
            errors.append(e)
        try:
            server.game.add_answer(filled_poll)
        except ValueError as e:
            errors.append(e)
        self.assertTrue(len(errors) == 2)
        self.assertTrue(server.game.user_data[user2][user1] is None)

    def test_fill_poll_two_answers(self):
        poll = server.load_poll(FILE_PATH)
        user1 = User(name="oilymacaroni")
        user2 = User(name="among us")

        server.game.register_user(user1)
        server.game.register_user(user2)

        server.game.start_polling_phase(poll)

        answer1 = Answer(question_name="q2", value=[QuestionOption() for _ in range(2)])
        filled_poll = FilledPoll(
            answers=[answer1, answer1], user_about=user1, user_filling=user2
        )
        errors = []
        try:
            server.game.validate_answers(filled_poll)
        except ValueError as e:
            errors.append(e)
        try:
            server.game.add_answer(filled_poll)
        except ValueError as e:
            errors.append(e)
        self.assertTrue(len(errors) == 2)
        self.assertTrue(server.game.user_data[user2][user1] is None)
