from abc import ABC, abstractmethod
from typing import Optional

class IGetAnswerConsumers(ABC):
    """
    Интерфейс для consumers, отвечающего за взаимодействие с ИИ помощником
    """

    @abstractmethod
    async def connect(self) -> None:
        """
        Установка соединения с клиентом через WebSocket
        Должен:
        - обрабатывать параметры подключения (student_id)
        - инициализировать соответствующий чат через ChatFactory
        - сохранять consumer в чате
        - завершать установку соединения
        """
        pass

    @abstractmethod
    async def disconnect(self, code: int) -> None:
        """
        Закрытие соединения с клиентом
        :param code: код закрытия соединения
        """
        pass

    @abstractmethod
    async def send_answer(self, text: str) -> None:
        """
        Отправка ответа от ИИ помощника клиенту
        :param text: текст ответа для отправки
        Должен:
        - отправить ответ в формате JSON с событием "answer"
        - закрыть соединение с кодом 200
        """
        pass