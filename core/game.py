from models.models import User


class Game:
    user_data: dict[User] = {}

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
        return self.remove_user(User(name=name))  # this works because users are hashed by user.name
