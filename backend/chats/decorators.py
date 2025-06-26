from functools import wraps

from rest_framework.response import Response
from rest_framework import status
from backend.settings import SECRET_KEY


def service_auth_required(view_func):
    """Проверка для апи эндпоинтов, ожидающих запросов от микросервиса"""
    @wraps(view_func)
    async def wrapper(request, *args, **kwargs):
        # Проверка токена из заголовка Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header or not auth_header.startswith('Service '):
            return Response(
                {"error": "Требуется авторизация сервиса"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = auth_header.split(' ')[1]
        if token != SECRET_KEY:
            return Response(
                {"error": "Неверный токен авторизации"},
                status=status.HTTP_403_FORBIDDEN
            )

        return await view_func(request, *args, **kwargs)
    return wrapper