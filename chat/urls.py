from django.urls import path
from . import views
urlpatterns = [
    path('chat/<int:group_id>', views.chat, name="chat"),
    path('chat/create', views.create_chat, name="create_chat")
]