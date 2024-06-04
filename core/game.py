import asyncio
from dataclasses import asdict

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from enum import IntEnum
from models.models import User, Poll, Answer, FilledPoll, QuestionTextbox
from typing import Dict, List


import json


class Phase(IntEnum):
    REGISTRATION = 1
    POLLING = 2
    ENDGAME = 3  # Nie mam pomysłu na inną nazwę


class Game:
    user_queues: Dict[User, asyncio.Queue] = {}
    user_data: Dict[User, Dict[User, List[Answer] | None]] = {}
    phase: Phase = Phase.REGISTRATION
    poll: Poll | None = None

    def __init__(self):
        self.user_update_queue = asyncio.Queue()

    def register_user(self, user: User, request: Request):
        if user in self.user_queues.keys():
            return False

        self.user_queues[user] = asyncio.Queue()
        self.user_data[user] = {}

        async def event_generator():
            try:
                while True:
                    # Wait for a new message to be available in the queue
                    message = await self.user_queues[user].get()
                    yield message
                    # If the client closes the connection, we break the loop
                    if await request.is_disconnected():
                        break
            except asyncio.CancelledError:
                pass

        self.user_queues[user].put_nowait("data: registered successfully\n\n")
        self.user_update_queue.put_nowait(self.list_users())
        return event_generator()

    def stream_users(self, request: Request):
        async def user_stream_generator():
            try:
                while True:
                    users = await self.user_update_queue.get()
                    # 
                    # Please don't use custom values for 'event' field.
                    # Browsers' EventSource.prototype.onmessage expects to receive messages with "event: message", so any other value will not work.
                    # This problem isn't reproducible with curl.
                    # Leaving this field empty, like in register_user() is fine. 
                    #
                    # yield f"event: lobbyUserListUpdate\ndata: {jsonable_encoder(users)}\n\n"
                    

                    # jsonable_encoder DOESN'T RETURN JSON STRING, IT TRANSFORMS OBJECT TO DICT WITH VALUES OF JSON-FRIENDLY VALUES!
                    # (source: https://fastapi.tiangolo.com/tutorial/encoder/)
                    # That's why we need to wrap the object with json.dumps()!

                    yield f"data: {json.dumps(jsonable_encoder(users))}\n\n"    
                    if await request.is_disconnected():
                        break

            except asyncio.CancelledError:
                pass

        self.user_update_queue.put_nowait(self.list_users())
        return user_stream_generator()

    def remove_user(self, user: User):
        if user in self.user_queues.keys():
            self.user_data.pop(
                user, None
            )  # prevents KeyError if it's not there for some reason
            self.user_queues.pop(user)
            self.user_update_queue.put_nowait(self.list_users())
            return True
        return False

    def remove_user_by_name(self, name: str):
        return self.remove_user(
            User(name=name)
        )  # this works because users are hashed by user.name

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

    def get_remaining_poll_targets(self, user: User) -> List[str]:
        """
        :param user: user for whom it is checked for which users answers are to be filled
        :return: list of user for whom polls are to be filled
        """
        return [
            person.name
            for person in self.user_data[user]
            if self.user_data[user][person] is None
        ]

    def get_answers_about(self, user: User) -> Dict[str, List[dict]]:
        return {u.name: [asdict(i) for i in self.user_data[u][user]]
                for u in self.user_data if (u != user and self.user_data[u][user] is not None)}

    def list_users(self) -> List[User]:
        """
        :return: list of users who joined game
        """
        return [user for user in self.user_data]

    def start_game(self):
        self.user_data = {
            k: {user: None for user in self.user_data if user is not k}
            for k, v in self.user_data.items()
        }
        self.phase = Phase.POLLING
        for queue in self.user_queues.values():
            queue.put_nowait("data: start\n\n")

    def end_game(self):
        for queue in self.user_queues.values():
            queue.put_nowait("end\n\n")
