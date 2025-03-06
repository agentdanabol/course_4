import hashlib


class User:
    def __init__(self, user_id: int, name: str, email: str, male: bool):
        self.__user_id = user_id
        self.__name = name
        self.__male = male
        self.__email = email
        self.__password_hash = None

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email

    @property
    def male(self) -> bool:
        return self.__male

    def set_password(self, password: str):
        self.__password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        return self.__password_hash == hashlib.sha256(password.encode()).hexdigest()
