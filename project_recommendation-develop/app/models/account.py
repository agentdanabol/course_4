class Account:
    def __init__(self, user_id: int, balance: float = 0.0):
        self.__user_id = user_id
        self.__balance = balance

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def balance(self) -> float:
        return self.__balance

    @balance.setter
    def balance(self, amount: float):
        if amount >= 0:
            self.__balance = amount
        else:
            raise ValueError("Баланс не может быть отрицательным")

    def deduct_balance(self, amount: float):
        if self.__balance >= amount:
            self.__balance -= amount
        else:
            raise ValueError("Недостаточно средств на балансе")

    def add_balance(self, amount: float):
        if amount > 0:
            self.__balance += amount
        else:
            raise ValueError("Сумма пополнения должна быть положительной")
