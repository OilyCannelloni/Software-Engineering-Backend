from enum import IntEnum

from models.models import User, Poll, Answer, FilledPoll, QuestionTextbox
from typing import Dict, List


class Phase(IntEnum):
    REGISTRATION = 1
    POLLING = 2
    ENDGAME = 3  # Nie mam pomysłu na inną nazwę


class Game:
    user_data: Dict[User, Dict[User, List[Answer] | None]] = {}
    phase: Phase = Phase.REGISTRATION
    poll: Poll | None = None

    def register_user(self, user: User):
        if user in self.user_data.keys():
            return False
        self.user_data[user] = {}
        return True

    def remove_user(self, user: User):
        if user in self.user_data.keys():
            self.user_data.pop(user)
            return True
        return False

    def remove_user_by_name(self, name: str):
        return self.remove_user(
            User(name=name)
        )  # this works because users are hashed by user.name

    def start_polling_phase(self, poll: Poll):
        self.user_data = {
            k: {user: None for user in self.user_data if user is not k}
            for k, v in self.user_data.items()
        }
        self.phase = Phase.POLLING
        self.poll = poll
        # raise NotImplementedError

    def validate_answers(self, filled_poll: FilledPoll) -> Exception | None:
        """
        Validates the
        :param filled_poll: check if the phase and users are correct
        :return:
        """
        if self.phase is not Phase.POLLING:
            raise AttributeError(
                "WRONG PHASE, PHASE MUST BE POLLING IN ORDER TO FILL A POLL"
            )
        if self.user_data[filled_poll.user_filling][filled_poll.user_about] is not None:
            raise KeyError(
                f"USER{filled_poll.user_filling.name}"
                f"HAS ALREADY FILLED A POLL ABOUT USER {filled_poll.user_about.name}"
            )
        answered = set()
        for answer in filled_poll.answers:
            answered.add(answer.question_name)
            empty_options = len(self.poll.questions[answer.question_name].options) == 0
            is_textbox = type(answer.value) is QuestionTextbox
            if empty_options != is_textbox:
                raise ValueError(f"ANSWER TO {answer.question_name} TYPE IS INCORRECT")
        for question_name, question in self.poll.questions.items():
            if not question.is_optional and question_name not in answered:
                raise ValueError(f"QUESTION {question_name} HAS TO BE ANSWERED")
        return None

    def add_answer(self, filled_poll: FilledPoll):
        """
        :param filled_poll: a poll filled by one user about another
        """
        self.validate_answers(filled_poll)
        self.user_data[filled_poll.user_filling][
            filled_poll.user_about
        ] = filled_poll.answers
        return True

    def get_remaining_poll_targets(self, user) -> List[User]:
        """
        :param user: user for whom it is checked for which users answers are to be filled
        :return: list of user for whom polls are to be filled
        """
        return [
            person
            for person in self.user_data[user]
            if self.user_data[user][person] is None
        ]

    def list_users(self) -> List[User]:
        """
        :return: list of users who joined game
        """
        return [user for user in self.user_data]
