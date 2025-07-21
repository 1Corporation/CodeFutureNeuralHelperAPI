"""
websocket routing
"""


from django.urls import path

from chats.consumers import GetAnswerConsumers



websocket_url_patterns = [
    path("websocket/v1/wait_answer/", GetAnswerConsumers.as_asgi()),
]
