from pydantic import BaseModel
from abc import ABC, abstractmethod


class User(BaseModel):
    name: str

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        return self.name == other.name


class Question(BaseModel, ABC):
    text: str

    @abstractmethod
    def get_answer_text(self) -> str:
        pass

    @abstractmethod
    def get_answer_details(self) -> dict[str, ...]:
        pass


class TextBoxQuestion(Question):
    textbox_content: str

    def get_answer_text(self) -> str:
        return self.textbox_content

    def get_answer_details(self) -> dict[str, ...]:
        return {"type": "textbox", "value": self.textbox_content}


class QuestionOption(BaseModel):
    text: str
    is_chosen: bool = False


class MultipleChoiceQuestion(Question):
    """
    For now, use this to model single choice questions as well.
    """
    options: list[QuestionOption]

    def get_answer_text(self):
        return "\n".join(opt.text for opt in self.options if opt.is_chosen)

    def get_answer_details(self) -> dict[str, ...]:
        return {"type": "multiple_choice", "value": [i for i, opt in enumerate(self.options) if opt.is_chosen]}


class Poll(BaseModel):
    title: str
    description: str
    questions: list[Question]
