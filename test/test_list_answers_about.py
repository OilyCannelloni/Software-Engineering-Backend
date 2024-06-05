import unittest

import test.common
from core.server import Server
from models.models import *
from routers import default_router

FILE_PATH = "file.json"
JSON_RESULT = """
{
    "among us": [
        {
            "question_name": "q1",
            "value": [
                {
                    "text": "",
                    "is_selected": false
                },
                {
                    "text": "",
                    "is_selected": false
                }
            ]
        },
        {
            "question_name": "q2",
            "value": {
                "is_visible": false,
                "initial_value": "",
                "value": ""
            }
        }
    ]
}
""".strip()


class TestListAnswersAbout(test.common.TestCaseCommonSetUpTwoUsersStartGame):
    def test_list_answers_about(self):
        answer1 = Answer(question_name="q1", value=[QuestionOption() for _ in range(2)])
        answer2 = Answer(question_name="q2", value=QuestionTextbox())
        filled_poll = FilledPoll(
            answers=[answer1, answer2], user_about=self.user1, user_filling=self.user2
        )

        self.server.game.add_answer(filled_poll)

        ans_about_1 = self.server.game.get_answers_about(self.user1)
        self.assertEqual(ans_about_1, {"among us": [answer1, answer2]})
        ans_about_2 = self.server.game.get_answers_about(self.user2)
        self.assertEqual(ans_about_2, {})

        json_ = json.dumps(
            self.server.game.get_answers_about(self.user1),
            default=lambda obj: obj.__dict__, indent=4
        )
        self.assertEqual(json_, JSON_RESULT)
