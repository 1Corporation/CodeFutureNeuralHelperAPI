from rest_framework.request import Request
from rest_framework.decorators import api_view
from asgiref.sync import sync_to_async


from abc import ABC, abstractmethod


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

