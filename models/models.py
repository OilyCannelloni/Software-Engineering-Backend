from __future__ import annotations
from enum import IntEnum
from typing import List, Dict

from pydantic import BaseModel, ValidationError
import json


class User(BaseModel):
    name: str

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        return self.name == other.name


class QuestionType(IntEnum):
    TEXTBOX = 1
    MULTIPLE_CHOICE = 2
    SINGLE_CHOICE = 3


class QuestionOption(BaseModel):
    text: str = ""
    is_selected: bool = False


class QuestionTextbox(BaseModel):
    is_visible: bool = False
    initial_value: str = ""
    value: str = ""


class Question(BaseModel):
    type: QuestionType
    text: str = ""
    textbox: QuestionTextbox = QuestionTextbox()
    options: list[QuestionOption] = []
    is_optional: bool = False


class Answer(BaseModel):
    question_name: str
    answer: str


class FilledPoll(BaseModel):
    answers: list[Answer]
    user_about: User
    user_filling: User


class PollDecodeError(Exception):
    pass


class Poll(BaseModel):
    title: str
    description: str
    questions: Dict[str, Question]

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_content) -> Poll:
        try:
            return Poll(**json.loads(json_content))
        except (ValidationError, TypeError, json.JSONDecodeError) as err:
            raise PollDecodeError from err


class SingleAnswer(BaseModel):
    respondentName: str
    answer: str


class SingleQuestionPollResults(BaseModel):
    question: str
    answers: List[SingleAnswer]


class SinglePersonPollResults(BaseModel):
    personName: str
    questions: List[SingleQuestionPollResults]


class PollResults(BaseModel):
    results: List[SinglePersonPollResults]
