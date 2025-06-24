"""
Общие API эндпоинты, которые нельзя присвоить конкретному сервису
"""


from rest_framework.decorators import api_view
from rest_framework.request import Request

from api.decorators import service_auth_required



@api_view(['GET'])
async def ping_ai(request: Request):
    """
    Отправьте запрос на этот эндпоинт и проверьте, готова ли нейросеть принимать запросы

    status 200 - нейросеть готова принимать запросы
    status 400 - нейросеть не может принимать запросы

    :param request:
    :return:
    """
    pass


@api_view(['GET'])
@service_auth_required
async def new_answer(request: Request):
    """
    Отправьте на этот эндпоинт ответ от ИИ, и направьте его пользователю
    Запрос требует сервисной авторизации по SECRET_KEY (смотри документацию декоратора service auth required
    """

    student_id = request.data.get("student_id")
    answer = request.data.get("answer")





