"""
Все представления rest api в сервисе chats
"""

from adrf.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from chats.service.chat_interface import ChatInterface
from chats.service.chat_factory import ChatFactory
from chats.decorators import service_auth_required

@api_view(['GET'])
async def get_chat_history(request: Request) -> Response:
    """
    Получить историю чата с помощником.

    Этот эндпоинт используется для получения истории взаимодействия студента с помощником.
    Перед тем как начать отправку сообщений помощнику, пользователь обязан сначала вызвать этот эндпоинт —
    он либо создаёт новый чат, либо возвращает уже существующий.

    Query Parameters:
        - student_id (str, required): Уникальный идентификатор студента.
        - course (str, required): Название или идентификатор курса.
        - timetable (str, required): Расписание студента.
        - full_name (str, required): Полное имя студента (используется при создании нового чата).

    Returns:
        Response: JSON-массив с историей сообщений в формате:
            [
                {"role": "user", "message": "Текст сообщения"},
                {"role": "assistant", "message": "Ответ помощника"},
                ...
            ]

    Status Codes:
        - 200 OK: История чата успешно получена.
        - 400 Bad Request: Отсутствует обязательный параметр student_id.
        - 500 Internal Server Error: Внутренняя ошибка при получении чата.

    Пример запроса:
        GET /api/chat/history/?student_id=12345&course=math101
    """

    student_id = request.query_params.get('student_id')
    course = request.query_params.get('course')
    timetable = request.query_params.get('timetable')
    full_name = request.query_params.get('full_name')

    # Получаем chat_history
    chat_factory = ChatFactory()
    chat: ChatInterface = chat_factory.get_or_create(
        student_id,
        course=course,
        timetable=timetable,
        full_name=full_name
    )

    return Response(chat.chat_history)


@api_view(["POST"])
async def receive_message(request: Request):
    """
    Принять сообщение от пользователя и передать его помощнику.

    Этот эндпоинт используется для отправки пользовательского сообщения в чат.
    После успешного запроса к этому эндпоинту пользователь обязан подключиться к WebSocket,
    по которому будут приходить обновления о статусах генерации ответа помощником.

    Body Parameters (application/json):
        - student_id (str, required): Уникальный идентификатор студента.
        - text (str, required): Текст сообщения от пользователя.

    Returns:
        Response: Пустой ответ с кодом статуса.

    Status Codes:
        - 200 OK: Сообщение успешно принято.
        - 404 Not Found: Чат не найден. Необходимо сначала выполнить запрос к `/api/v1/chat_history/`.

    Пример запроса:
        POST /api/v1/receive_message/
        {
            "student_id": "12345",
            "text": "Привет, расскажи про расписание"
        }

    Примечание:
        После вызова этого эндпоинта необходимо установить WebSocket-соединение,
        чтобы отслеживать прогресс и получение ответа от помощника.
    """

    student_id = request.data.get('student_id')
    text = request.data.get("text")

    # Получаем chat_history
    chat_factory = ChatFactory()


    # TODO: Ошибка почему-то не вызывается
    try:
        chat: ChatInterface = chat_factory.get_or_create(student_id)
    except TypeError:
        return Response(
            data={"comment": "Chat not found. First, send a request to /api/v1/chat_history."},
            status=HTTP_404_NOT_FOUND)

    await chat.receive_message(text)
    return Response(status=HTTP_200_OK)


@api_view(['POST'])
@service_auth_required
async def send_message(request: Request) -> Response:
    """
    Отправить сообщение от помощника в чат студента.

    Эндпоинт используется для отправки сообщения **от имени помощника**.
    Может применяться для ручной отправки системных сообщений или ответов, сформированных заранее.

    Body Parameters (application/json):
        - student_id (str, required): Уникальный идентификатор студента.
        - text (str, required): Текст сообщения от помощника.

    Headers:
        - Authorization: Service + SECRET_KEY

    Returns:
        Response: Пустой ответ с кодом статуса.

    Status Codes:
        - 200 OK: Сообщение успешно отправлено.
        - 404 Not Found: Чат не найден. Необходимо сначала выполнить запрос к `/api/v1/chat_history/`.

    Пример запроса:
        POST /api/v1/send_message/
        {
            "student_id": "12345",
            "text": "Ваш запрос принят. Ожидайте ответа."
        }

        + Headers

        {
            "Authorization": Service `SECRET_KEY`
        }

    Примечание:
        Этот метод напрямую вставляет сообщение в историю чата от имени помощника без генерации или подтверждения.
    """

    student_id = request.data.get('student_id')
    text = request.data.get("text")
    print(text)

    # Получаем chat_history
    chat_factory = ChatFactory()

    try:
        chat: ChatInterface = chat_factory.get_or_create(student_id)
    except TypeError:
        return Response(
            data={"comment": "Chat not found. First, send a request to /api/v1/chat_history."},
            status=HTTP_404_NOT_FOUND)

    await chat.send_message(text)
    return Response(status=HTTP_200_OK)
