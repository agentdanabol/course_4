from user import User
from account import Account
from prediction import PredictionHistory


class UserService:
    __users = {}
    __accounts = {}

    @classmethod
    def register_user(cls, name: str, email: str, male: bool, password: str) -> User:
        user_id = len(cls.__users) + 1
        user = User(user_id, name, email, male)
        user.set_password(password)
        cls.__users[user_id] = user
        cls.__accounts[user_id] = Account(user_id)
        return user

    @classmethod
    def get_user(cls, user_id: int) -> User:
        return cls.__users.get(user_id)

    @classmethod
    def get_account(cls, user_id: int) -> Account:
        return cls.__accounts.get(user_id)


class HistoryService:
    __history = []

    @classmethod
    def add_history(cls, history):
        cls.__history.append(history)

    @classmethod
    def get_user_history(cls, user_id: int):
        return [h for h in cls.__history if h.user_id == user_id]

    @classmethod
    def generate_history_id(cls) -> int:
        return len(cls.__history) + 1
