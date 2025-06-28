from django.urls import path

from chats.views import get_chat_history, send_message, receive_message

urlpatterns = [
    path('get_chat_history', get_chat_history, name='get_chat_history'),
    path('send_message', send_message, name='send_message'),
    path('receive_message', receive_message, name='receive_message')
]