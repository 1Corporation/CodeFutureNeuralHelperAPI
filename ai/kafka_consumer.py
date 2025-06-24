"""
Работа с kafka
"""

from typing import Optional
import json
import requests

from confluent_kafka import Consumer, Message, KafkaException

from ai_process import process

HOST = "daphne:8000"


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
        value: Optional[str] = msg.value(None)

        if value is None:
            raise RuntimeError("content in message is None!")

        if msg.error():
            raise KafkaException(msg.error())

        json_message: dict = json.loads(value)
        answer: str = process(json_message)

        # отправка ответа
        data = {"student_id": json_message["student_id"], "answer": answer}
        requests.post("http://" + HOST + "/api/v1/answer/", data=json.dumps(data))


    def run(self) -> None:
        """
        Запустите бесконечный цикл в котором будут обрабатываться запросы
        :return:
        """
        self.flag = True
        while self.flag:
            self.__consume_message()
