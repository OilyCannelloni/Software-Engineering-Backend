import pathlib
import unittest
from models.models import *
from core.server import server

FILE_PATH = "test-poll-load-save-1"


class TestPollLoadSave(unittest.TestCase):
    def test_poll_load_save(self):
        q1 = Question(text="Question 1", type=QuestionType.MULTIPLE_CHOICE, options=[
            QuestionOption(text="opt 1"),
            QuestionOption(text="opt 2", is_optional=True)
        ])
        q2 = Question(text="Question 2", type=QuestionType.TEXTBOX,
                      textbox=QuestionTextbox(initial_value="init_val"))
        poll = Poll(
            title="Test Poll",
            description="Testing JSON serialization",
            questions=[q1, q2]
        )

        try:
            server.save_poll(poll, FILE_PATH)
            poll = server.load_poll(FILE_PATH)
        finally:
            pathlib.Path(FILE_PATH).unlink(missing_ok=True)

        self.assertEqual(poll.title, "Test Poll")
        self.assertEqual(poll.description, "Testing JSON serialization")
        self.assertEqual(poll.questions[0].textbox.is_visible, False)
        self.assertEqual(poll.questions[0].type, QuestionType.MULTIPLE_CHOICE)
        self.assertEqual(len(poll.questions), 2)
        self.assertEqual(poll.questions[0].options[0].text, "opt 1")
        self.assertEqual(len(poll.questions[0].options), 2)
        self.assertEqual(len(poll.questions[1].options), 0)