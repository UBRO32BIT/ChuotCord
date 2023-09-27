from django.urls import path
from .views import ChatView, CreateChatView, DeleteChatView, AddUserToGroupView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('chat/<int:group_id>/', login_required(ChatView.as_view()), name='chat'),
    path('chat/create', login_required(CreateChatView.as_view()), name='create_chat'),
    path('chat/delete/<int:group_id>/', login_required(DeleteChatView.as_view()), name='delete_chat'),
    path('invite/<str:invite_str>/', login_required(AddUserToGroupView.as_view()), name='invite'),
]