import asyncio
from models.models import User
from fastapi import Request


class Game:
    user_data: dict[User, asyncio.Queue] = {}

    def register_user(self, user: User, request: Request):
        if user in self.user_data.keys():
            return False

        self.user_data[user] = asyncio.Queue()

        async def event_generator():
            try:
                while True:
                    # Wait for a new message to be available in the queue
                    message = await self.user_data[user].get()
                    yield message
                    # If the client closes the connection, we break the loop
                    if await request.is_disconnected():
                        break
            except asyncio.CancelledError:
                pass

        self.user_data[user].put_nowait("data: registered successfully\n\n")
        return event_generator()

    def remove_user(self, user: User):
        if user in self.user_data.keys():
            self.user_data.pop(user)
            return True
        return False

    def remove_user_by_name(self, name: str):
        return self.remove_user(User(name=name))  # this works because users are hashed by user.name

    def start_game(self):
        for queue in self.user_data.values():
            queue.put_nowait("start\n\n")

    def end_game(self):
        for queue in self.user_data.values():
            queue.put_nowait("end\n\n")

