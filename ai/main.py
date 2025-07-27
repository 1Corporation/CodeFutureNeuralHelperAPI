"""
Пишите код в этом проекте в синхронном контексте
"""

from kafka_consumer import KafkaConsumer

from message_validator import MessageValidator


def main() -> None:
    """
    a main script
    :return: None
    """

    MessageValidator()  # Инициализируем валидатор заранее, см документацию

    kafka_instance = KafkaConsumer()
    kafka_instance.run()

if __name__ == '__main__':
    main()