from pydantic import BaseModel
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class User(BaseModel):
    name: str


@dataclass
class Question(BaseModel, ABC):
    text: str

    @abstractmethod
    def get_answer_text(self):
        pass


@dataclass
class TextBoxQuestion(Question):
    textbox_content: str

    def get_answer_text(self):
        return self.textbox_content


@dataclass
class QuestionOption(BaseModel):
    text: str
    is_chosen: bool = False


@dataclass
class MultipleChoiceQuestion(Question):
    """
    For now, use this to model single choice questions as well.
    """
    options: list[QuestionOption]

    def get_answer_text(self):
        return "\n".join(opt.text for opt in self.options if opt.is_chosen)


@dataclass
class Poll(BaseModel):
    title: str
    description: str
    questions: list[Question]
