from django.urls import path
from .views import chat_view
from .views import registerStaff, forgot_password, register, verify_code, password_reset, EmployeeListView, EmployerListView, EmployeeDeleteView, EmployerDeleteView, StaffListView, StaffDeleteView

urlpatterns = [
    path('chat/', chat_view),
    path('api/user-list/', EmployeeListView.as_view(), name='employee-list'),
    path('api/company-list/', EmployerListView.as_view(), name='employer-list'),
    path('api/staff-list/', StaffListView.as_view(), name='staff-list'),
    path('api/employee/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('api/employer/<int:pk>/delete/', EmployerDeleteView.as_view(), name='employer-delete'),
    path('api/staff/<int:pk>/delete/', StaffDeleteView.as_view(), name='staff-delete'),
    path('register-staff/', registerStaff, name='register-staff'),
    path('register-user/', register, name='register-user'),
    path('api/forgot-password/', forgot_password, name='forgot-password'),
    path('api/verify-code/', verify_code, name='verify-code'),
    path('api/reset-password/', password_reset, name='password-reset'),

]   