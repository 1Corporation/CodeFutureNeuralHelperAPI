"""
Пишите код в этом проекте в синхронном контексте
"""

from kafka_consumer import KafkaConsumer


def main() -> None:
    """
    a main script
    :return: None
    """

    kafka_instance = KafkaConsumer()
    kafka_instance.run()

if __name__ == '__main__':
    main()