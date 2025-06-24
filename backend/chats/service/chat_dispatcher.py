"""ChatDispatcher"""


from typing import Dict, Optional

from chats.service.chat_interface import ChatInterface

class ChatDispatcher:
    """
    Регистр существующих чатов. Поддерживает добавление в регистр новых, удаление старых, и получения объектов чата.
    Так же выполняет другую бизнес-логику, например контролирует количество чатов.
    Гарантирует то что экземпляр чата для конктретного студента всего один
    """

    def __init__(self):
        self.__chats: Dict[int, ChatInterface] = {}


    def get_chat(self, student_id: int) -> Optional[ChatInterface]:
        """
        Получить чат по id студента
        :param student_id: УНТИ студента
        :return: Чат студента
        """
        return self.__chats.get(student_id)


    def add_chat(self, student_id: int, chat: ChatInterface) -> None:
        """
        Добавить чат в диспетчера
        :param student_id: УНТИ студента
        :param chat: Объект чата
        """

        if self.__chats.get(student_id) is not None:
            raise RuntimeError("Попытка создать новый чат для студента, когда он уже существует")

        self.__chats[student_id] = chat


    def delete_chat(self, student_id: int) -> None:
        """
        Удалить чат из диспетчера
        :param student_id: УНТИ студента
        """

        del self.__chats[student_id]