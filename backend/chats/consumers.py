"""
Channels consumers для сервиса chats
"""


import urllib.parse

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chats.service.chat_factory import ChatFactory
from chats.service.chat_interface import ChatInterface
from chats.consumer_interface import IGetAnswerConsumers



class GetAnswerConsumers(AsyncJsonWebsocketConsumer, IGetAnswerConsumers):
    """
    Консьюмер отвечающий за получение ответа от ИИ помощника
    Обновления и прочее
    """


    async def connect(self):
        """
        override consumer connect method
        """

        # Получаем student_id
        query_string = self.scope["query_string"].decode()
        query_params = urllib.parse.parse_qs(query_string)
        student_id = query_params.get("student_id", [None])[0]

        # Устанавливаем consumer для 
        chat_factory: ChatFactory = ChatFactory()
        try:
            chat: ChatInterface = chat_factory.get_or_create(student_id)
        except TypeError:
            # TODO: Отклони на этапе HTTP
            await self.close(code=4004, reason="Chat not found. First, send a request to /api/v1/chat_history.")
            return

        if not chat.is_wait:
            await self.close(code=4003, reason="User doesn't wait answer by AI. First, send request to /api/v1/receive_message")
            return

        chat.set_consumer(self)

        await self.accept()


    async def disconnect(self, code):
        """
        override consumer disconnect method
        """
        await self.close(code)


    async def send_answer(self, text):
        """
        Отправить студенту ответ от помощника
        """

        await self.send_json({"event": "answer", "text": text})
        await self.disconnect(1000)


