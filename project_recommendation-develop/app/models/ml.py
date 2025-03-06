from item import ClothingItem
from prediction import PredictionRequest, PredictionHistory
from services import UserService, HistoryService
from settings import EXECUTION_COST
from account import Account


class MLModel:
    def __init__(self, model_id: int, name: str):
        self.__model_id = model_id
        self.__name = name

    @property
    def model_id(self) -> int:
        return self.__model_id

    @property
    def name(self) -> str:
        return self.__name

    def predict(self, clothing_items: list[ClothingItem]) -> ClothingItem:
        #Здесь будет логика предсказания
        #TODO
        if clothing_items:
            return clothing_items[0]
        raise ValueError("Список вещей для предсказания пуст")


class MLTask:
    def __init__(self, task_id: int, user_id: int, request: PredictionRequest, model: MLModel):
        self.__task_id = task_id
        self.__user_id = user_id
        self.__request = request
        self.__model = model

    def execute(self) -> ClothingItem:
        # Проверка баланса пользователя
        user = UserService.get_user(self.__user_id)
        user_account = UserService.get_account(self.__user_id)

        if not user or not user_account:
            raise ValueError("Пользователь или аккаунт не найден")

        try:
            if user_account.balance >= EXECUTION_COST:
                user_account.deduct_balance(EXECUTION_COST)
                predicted_item = self.__model.predict(self.__request.clothing_items)

                history = PredictionHistory(
                    history_id=HistoryService.generate_history_id(),
                    user_id=self.__user_id,
                    request_id=self.__request.request_id,
                    predicted_item=predicted_item,
                    cost=EXECUTION_COST
                )
                HistoryService.add_history(history)
                return predicted_item
            else:
                raise ValueError("Недостаточно средств на балансе")
        except ValueError as e:
            # Откат операции при ошибке
            user_account.add_balance(EXECUTION_COST)
            raise e