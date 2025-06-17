"""
ChatFactory класс
"""
from typing import Optional

from ai_helper.chats.service.chat_dispatcher import ChatDispatcher
from ai_helper.chats.service.chat_interface import ChatInterface
from ai_helper.chats.service.in_memory_chat import InMemoryChat


class ChatFactory:
    """
    Сочетает в себе паттерн Factory и Dispatcher, задача создавать и раздавать объекты ChatInterface
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(ChatFactory, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True
            self.__init()


    def __init(self):
        """
        Из python документации при подобной реализации паттерна,
        конструктор должен иметь название __init, вместо обычного конструктора
        """

        self.__dispatcher = ChatDispatcher()

    def get_or_create(self, student_id: int, **kwargs) -> ChatInterface:
        """
        Фабричный метод
        :param student_id: УНТИ студента
        :param args: Аргументы нужные для инициализации чата (Смотри конструктор конкретного чата). Используется в случае если в ChatDispatcher нету чата со студентом с УНТИ student_id
        :return: объект типа ChatInterface
        """

        chat: Optional[ChatInterface]  = self.__dispatcher.get_chat(student_id)

        if chat is not None:
            return chat

        # warning! Concrete chat.
        chat: ChatInterface = InMemoryChat(student_id, **kwargs)
        return chat
