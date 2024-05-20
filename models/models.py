from __future__ import annotations
from enum import Enum
from pydantic import BaseModel
import json


class User(BaseModel):
    name: str

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        return self.name == other.name


class QuestionType(Enum):
    TEXTBOX = 1
    MULTIPLE_CHOICE = 2
    SINGLE_CHOICE = 3


class QuestionOption(BaseModel):
    text: str
    is_selected: bool = False


class QuestionTextbox(BaseModel):
    is_visible: bool = False
    initial_value: str = ""
    value: str = ""


class Question(BaseModel):
    type: QuestionType
    text: str
    textbox: QuestionTextbox = QuestionTextbox()
    options: list[QuestionOption] = []
    is_optional: bool

    def get_answer_text(self) -> str:
        if self.type == QuestionType.MULTIPLE_CHOICE or self.type == QuestionType.SINGLE_CHOICE:
            return "\n".join(opt.text for opt in self.options if opt.is_selected)
        if self.type == QuestionType.TEXTBOX:
            return self.textbox.value
        return ""


class Poll(BaseModel):
    title: str
    description: str
    questions: list[Question]

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_content) -> Poll:
        return Poll(**json.loads(json_content))
