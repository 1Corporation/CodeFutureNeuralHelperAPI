"""
InMemoryChat реализация
"""

from typing import List, Dict

from ai_helper.chats.service.chat_interface import ChatInterface


class InMemoryChat(ChatInterface):
    """
    in-memory реализация чата. Реализует ChatInterface
    """



    def __init__(self,
               student_id,
               full_name: str = None,
               timetable: dict = None,
               course: str = None,
               ) -> None:
        """


        :param student_id: УНТИ студента
        :param full_name: ФИО студента
        :param timetable: расписание студента
        :param course: курс на котором обучается студент (1С:Исполнитель или Python)

        :return: None
        """

        self.__student_id: int = student_id
        self.__full_name: str = full_name
        self.__timetable: dict = timetable
        self.__course: str = course
        self.__chat_history: List[Dict[str, str]] = []

    def send_message(self, text: str) -> None:
        """
        Добавить сообщение в историю сообщений, отправить пользователю, закрыть сокет
        Остальное см. в документации интерфейса
        :param text: сообщение ИИ помощника
        """

        self.__new_message(text, "helper")
        # TODO: реализуй обновление чата и закрытие сокета

    def receive_message(self, text) -> None:
        """
        Получить сообщение, добавить в историю сообщений, отправить запрос нейросети и открыть сокет.
        Остальное см. в документации интерфейса
        :param text: текст сообщения
        """
        self.__new_message(text, "student")
        # TODO: реализуй запрос в нейросеть и открытие сокета

    def delete_chat(self) -> None:
        """
        Поведение при удалении чата
        Остальное см. в документации интерфейса
        """
        pass

    def __new_message(self, text: str, role: str) -> None:
        """
        Создайте новое сообщение в чате
        :param text: текст сообщения
        :param role: кто отправил сообщение
        """

        message = {"text": text, role: role}
        self.__chat_history.append(message)


    @property
    def chat_history(self):
        """
        История чатов не может быть изменена, но должна быть доступна из вне
        :return: история чатов
        """

        return self.__chat_history