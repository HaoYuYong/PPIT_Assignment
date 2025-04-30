from django.urls import path
from .views import chat_view
from .views import forgot_password
from .views import EmployeeListView, EmployerListView

urlpatterns = [
    path('chat/', chat_view),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('api/staff-user-list/', EmployeeListView.as_view(), name='employee-list'),
    path('api/staff-user-list/', EmployerListView.as_view(), name='employer-list'),
    path('api/admin-user-list/', EmployeeListView.as_view(), name='employee-list'),
    path('api/admin-user-list/', EmployerListView.as_view(), name='employer-list'),
]