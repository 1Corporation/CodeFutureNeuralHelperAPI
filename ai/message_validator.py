"""
MessageValidator class
"""

import re


class MessageValidator(object):
    """
    Валидатор сообщений, для валидации используйте метод validate
    Использует Singleton pattern
    Создайте инстанкцию этого объекта при запуске сервера, для компиляции всех паттернов
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(MessageValidator, cls).__new__(cls, *args, **kwargs)
            cls._initialized = False
        return cls._instance

    def __init__(self):
        if not self.__class__._initialized:
            self.__class__._initialized = True  # set initial flag to True
            self.__init()

    def __init(self):
        """
        В Singleton этот метод должен выполнять функции конструктора
        :return:
        """
        self.__banwords_pattern: re.Pattern = self.__get_banwords_regex_pattern()
        self.__profanity_pattern: re.Pattern = self.__get_profanity_regex_pattens()
        self.__chars_pattern: re.Pattern = self.__get_chars_regex_pattern()

    def __get_banwords_regex_pattern(self) -> re.Pattern:
        """
        :return: re.Pattern с запрещенными словами
        """

        with open("banwords_regex.txt", "r", encoding="utf-8") as file:
            regex = file.read()
            return re.compile(regex, re.IGNORECASE | re.UNICODE)

    def __get_profanity_regex_pattens(self) -> re.Pattern:
        """
        :return: re.Pattern с матами
        """

        with open("profanity_regex.txt", "r", encoding="utf-8") as file:
            regex = file.read()
            return re.compile(regex, re.IGNORECASE | re.UNICODE)

    def __get_chars_regex_pattern(self) -> re.Pattern:
        """
        :return: re.Pattern на символы
        """

        regex = r'^[a-zA-Zа-яА-ЯёЁ0-9\s\.,!?\-\+\*\/\(\)\[\]\{\}\"\':;@#%&_=<>`~$^]+$'
        return re.compile(regex, re.IGNORECASE | re.UNICODE)


    def validate(self, message: str) -> bool:
        """
        Проверит сообщение на наличие нарушений
        :param message: текст сообщений
        :return: True, если сообщение успешно прошло проверку
        """

        chars_check = not bool(self.__chars_pattern.search(message))
        profanity_check = bool(self.__profanity_pattern.search(message))
        banwords_check = bool(self.__banwords_pattern.search(message))

        return not (chars_check or profanity_check or banwords_check)
