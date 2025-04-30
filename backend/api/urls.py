from django.urls import path
from .views import chat_view
from .views import forgot_password

urlpatterns = [
    path('chat/', chat_view),
    path('forgot-password/', forgot_password),
]