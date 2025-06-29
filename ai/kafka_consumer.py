"""
Работа с kafka
"""

import os
from typing import Optional
import json
import requests
from dotenv import load_dotenv

from confluent_kafka import Consumer, Message, KafkaException

from ai_process import process

load_dotenv()

HOST = "backend:8000"
SECRET_KEY = os.getenv("SECRET_KEY")

class KafkaConsumer:
    """
        Настройка над confluent_kafka.Consumer для удобного управления консьюмером
    """

    def __init__(self):
        self.__consumer = Consumer({
            'bootstrap.servers': 'kafka:9092',
            'group.id': 'ai-group',
            'auto.offset.reset': 'earliest'
        })

        self.__consumer.subscribe(['ai-topic'])
        self.flag = False

    def __consume_message(self):
        """
        Получить сообщение от kafka и сгенерировать ответ
        :return:
        """

        msg: Message = self.__consumer.poll()

        # Обработка сообщения
        value: Optional[str] = msg.value()

        if value is None:
            raise RuntimeError("content in message is None!")

        if msg.error():
            raise KafkaException(msg.error())

        json_message: dict = json.loads(value)
        answer: str = process(json_message)

        # отправка ответа
        data = {"student_id": json_message["student_id"], "text": answer}
        requests.post(
            "http://" + HOST + "/api/v1/send_message",
            data=json.dumps(data),
            headers = {"Authorization": "Service " + SECRET_KEY,
                       "Content-Type": "application/json"})


    def run(self) -> None:
        """
        Запустите бесконечный цикл в котором будут обрабатываться запросы
        :return:
        """
        self.flag = True
        while self.flag:
            self.__consume_message()
