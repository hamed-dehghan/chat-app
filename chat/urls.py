# urls.py
from django.urls import path
from .views import CreateChatView, OTPLogin, UserListView
from .views import ChatMessageListView

urlpatterns = [
    path('api/chats/messages/', ChatMessageListView.as_view(), name='chat_messages'),
    path('api/chats/create/', CreateChatView.as_view(), name='chat-create'),
    path('api/chats/users/', UserListView.as_view(), name='chat-users'),
    path('api/chats/previous-users/', UserListView.as_view(), name='chat-users'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/auth/login/', OTPLogin.as_view(), name='otp_login'),
]
