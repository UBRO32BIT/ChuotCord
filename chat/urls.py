from django.urls import path
from . import views
urlpatterns = [
    path('chat/<int:group_id>', views.chat, name="chat")
]