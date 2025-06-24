

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from chats.service import ChatInterface, ChatFactory


@api_view(['GET'])
async def get_chat_history(request: Request) -> Response:
    """
    Получить историю чата с помощником

    :param request: restframework.request.Request
    :return: историю чата как restframework.response.Response
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


@api_view(['POST'])
async def send_message(request: Request) -> Response:
    """
    Отправить сообщение в чат с помощником
    :param request: restframework.request.Request
    :return: restframework.response.Response
    """

    student_id = request.data.get('student_id')
    course = request.data.get('course')
    timetable = request.data.get('timetable')
    full_name = request.data.get('full_name')
    text = request.data.get("text")


    # Получаем chat_history
    chat_factory = ChatFactory()
    chat: ChatInterface = chat_factory.get_or_create(
        student_id,
        course=course,
        timetable=timetable,
        full_name=full_name
    )

    chat.send_message(text)

    # TODO: создай другие статусы и опиши в документации
    return Response(200)


