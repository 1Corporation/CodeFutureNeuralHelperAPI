"""
ChatInterface
"""


from abc import ABC, abstractmethod

class ChatInterface(ABC):
    """
    Все классы чатов должны реализовывать этот интерфейс
    """

    @abstractmethod
    def send_message(self, text) -> None:
        """
        Отправить сообщение в чат от имени нейросети
        :param text: текст сообщения
        """
        pass

    @abstractmethod
    def receive_message(self, text) -> None:
        """
        Получить сообщение от студента
        :param text: текст сообщения
        """
        pass

    @abstractmethod
    def delete_chat(self) -> None:
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