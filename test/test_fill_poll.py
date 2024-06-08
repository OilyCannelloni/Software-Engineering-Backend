from models.models import *
from test.common import TestCaseCommonSetUpTwoUsersStartGame


class TestFillPoll(TestCaseCommonSetUpTwoUsersStartGame):
    def test_fill_poll(self):
        answer1 = Answer(question_name="q1", value=[QuestionOption() for _ in range(2)])
        answer2 = Answer(question_name="q2", value=QuestionTextbox())
        filled_poll = FilledPoll(
            answers=[answer1, answer2], user_about=self.user1, user_filling=self.user2
        )

        validation = self.server.game.validate_answers(filled_poll)
        result = self.server.game.add_answer(filled_poll)
        self.assertTrue(validation is None)
        self.assertTrue(result)
        self.assertTrue(self.server.game.user_data[self.user2][self.user1] is not None)
        self.assertTrue(len(self.server.game.user_data[self.user2][self.user1]) == 2)

    def test_fill_poll_bad_answer(self):
        answer1 = Answer(question_name="q2", value=[QuestionOption() for _ in range(2)])
        answer2 = Answer(question_name="q1", value=QuestionTextbox())
        filled_poll = FilledPoll(
            answers=[answer1, answer2], user_about=self.user1, user_filling=self.user2
        )
        errors = []
        try:
            self.server.game.validate_answers(filled_poll)
        except ValueError as e:
            errors.append(e)
        try:
            self.server.game.add_answer(filled_poll)
        except ValueError as e:
            errors.append(e)
        self.assertTrue(len(errors) == 2)
        self.assertTrue(self.server.game.user_data[self.user2][self.user1] is None)

    def test_fill_poll_two_answers(self):
        answer1 = Answer(question_name="q2", value=[QuestionOption() for _ in range(2)])
        filled_poll = FilledPoll(
            answers=[answer1, answer1], user_about=self.user1, user_filling=self.user2
        )
        errors = []
        try:
            self.server.game.validate_answers(filled_poll)
        except ValueError as e:
            errors.append(e)
        try:
            self.server.game.add_answer(filled_poll)
        except ValueError as e:
            errors.append(e)
        self.assertTrue(len(errors) == 2)
        self.assertTrue(self.server.game.user_data[self.user2][self.user1] is None)
