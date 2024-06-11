import unittest

from models.models import Poll, Question, QuestionOption, QuestionTextbox, QuestionType

JSON_STR = """
{
    "title": "Test Poll",
    "description": "Testing JSON serialization",
    "questions": {
        "q1": {
            "type": 2,
            "text": "Question 1",
            "textbox": {
                "is_visible": false,
                "initial_value": "",
                "value": ""
            },
            "options": [
                {
                    "text": "opt 1",
                    "is_selected": false
                },
                {
                    "text": "opt 2",
                    "is_selected": false
                }
            ],
            "is_optional": false
        },
        "q2": {
            "type": 1,
            "text": "Question 2",
            "textbox": {
                "is_visible": false,
                "initial_value": "init_val",
                "value": ""
            },
            "options": [],
            "is_optional": false
        }
    }
}
""".strip()


class TestPollToJson(unittest.TestCase):
    def test_poll_to_json(self):
        q1 = Question(
            text="Question 1",
            type=QuestionType.MULTIPLE_CHOICE,
            options=[
                QuestionOption(text="opt 1"),
                QuestionOption(text="opt 2", is_optional=True),
            ],
        )
        q2 = Question(
            text="Question 2",
            type=QuestionType.TEXTBOX,
            textbox=QuestionTextbox(initial_value="init_val"),
        )
        poll = Poll(
            title="Test Poll",
            description="Testing JSON serialization",
            questions={"q1": q1, "q2": q2},
        )

        json_content = poll.to_json()

        self.assertEqual(json_content, JSON_STR)

    def test_poll_from_json(self):
        poll: Poll = Poll.from_json(JSON_STR)

        self.assertEqual(poll.title, "Test Poll")
        self.assertEqual(poll.description, "Testing JSON serialization")
        self.assertEqual(poll.questions["q1"].textbox.is_visible, False)
        self.assertEqual(len(poll.questions), 2)
        self.assertEqual(poll.questions["q1"].options[0].text, "opt 1")
        self.assertEqual(len(poll.questions["q1"].options), 2)
        self.assertEqual(len(poll.questions["q2"].options), 0)
