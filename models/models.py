from pydantic import BaseModel


class User(BaseModel):
    name: str

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        return self.name == other.name


class QuestionOption(BaseModel):
    text: str
    is_chosen: bool = False


class QuestionTextbox(BaseModel):
    is_visible: bool = False
    initial_value: str = ""
    value: str = ""


class Question(BaseModel):
    text: str
    textbox: QuestionTextbox = QuestionTextbox()
    options: list[QuestionOption] = []

    def get_answer_text(self) -> str:
        ans = "\n".join(opt.text for opt in self.options if opt.is_chosen)
        if self.textbox.is_visible:
            ans += f"\n\n{self.textbox.value}"
        return ans


class Poll(BaseModel):
    title: str
    description: str
    questions: list[Question]
