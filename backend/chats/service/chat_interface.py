"""
ChatInterface
"""

from typing import Optional
from abc import ABC, abstractmethod

from channels.consumer import AsyncConsumer


class ChatInterface(ABC):
    """
    Все классы чатов должны реализовывать этот интерфейс
    """

    @abstractmethod
    async def send_message(self, text) -> None:
        """
        Отправить сообщение в чат от имени нейросети
        :param text: текст сообщения
        """
        pass

    @abstractmethod
    async def receive_message(self, text) -> None:
        """
        Получить сообщение от студента
        :param text: текст сообщения
        """
        pass

    @abstractmethod
    async def delete_chat(self) -> None:
        """
        Поведение объекта чата при его удалении
        """
        pass

    @property
    @abstractmethod
    def chat_history(self) -> list:
        """
        История чатов не может быть изменена, но должна быть доступна из вне
        :return: история чатов
        """
        pass

    @abstractmethod
    def set_consumer(self, consumer: Optional[AsyncConsumer]) -> None:
        """
        Установите consumer для chat
        """
        pass

    @property
    @abstractmethod
    def is_wait(self) -> bool:
        """
        Верните статус чата, находится ли в он в ожидании ответа
        """
        pass

    @property
    @abstractmethod
    def last_request_time(self) -> int:
        """
        getter последнего запроса к нейросети
        """
        pass