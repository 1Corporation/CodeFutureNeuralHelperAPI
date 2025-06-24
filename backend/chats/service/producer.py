"""
Описание kafka-продюсера для сервиса chats
"""

import json

from confluent_kafka import Producer


class KafkaProducer:
    """
    Предоставляет удобный интерфейс для работы с kafka продюсером и хранит его инстанс
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(KafkaProducer, cls).__new__(cls, *args, **kwargs)
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

        self.__producer = Producer({"bootstrap.servers": "kafka:9092"})
        self.__topic = "ai-topic"

    def produce_new_message(self, **kwargs):
        """
        Отправь сообщение консьюмеру
        """
        data = json.dumps(kwargs)
        self.__producer.produce(self.__topic, value=data)
