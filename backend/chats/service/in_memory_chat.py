"""
InMemoryChat реализация
"""

from typing import List, Dict, Optional

from channels.consumer import AsyncConsumer

from chats.service.chat_interface import ChatInterface
from chats.service.producer import KafkaProducer
from chats.consumer_interface import IGetAnswerConsumers

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
        self.__websocket_consumer: Optional[IGetAnswerConsumers] = None

    async def send_message(self, text: str) -> None:
        """
        Добавить сообщение в историю сообщений, отправить пользователю, закрыть сокет
        Остальное см. в документации интерфейса
        :param text: сообщение ИИ помощника
        """

        self.__new_message(text, "helper")
        await self.__websocket_consumer.send_answer(text)
        self.__websocket_consumer = None

    async def receive_message(self, text) -> None:
        """
        Получить сообщение, добавить в историю сообщений, отправить запрос нейросети и открыть сокет.
        Остальное см. в документации интерфейса
        :param text: текст сообщения
        """
        self.__new_message(text, "student")

        await KafkaProducer().produce_new_message(
            chat=self.__chat_history,
            student_id=self.__student_id,
            full_name=self.__full_name,
            timetable=self.__timetable,
            course=self.__course
        )

    async def delete_chat(self) -> None:
        """
        Поведение при удалении чата
        Остальное см. в документации интерфейса
        """

        await self.__websocket_consumer.disconnect(200)
        self.__websocket_consumer = None

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

    def set_consumer(self, consumer: Optional[AsyncConsumer]) -> None:
        """
        Установите consumer
        """
        self.__websocket_consumer = consumer
