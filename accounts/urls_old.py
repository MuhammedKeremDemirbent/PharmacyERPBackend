from django.urls import path
from .views import RegisterEmployeeView, UserListCreateView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('register-employee/', RegisterEmployeeView.as_view(), name='register-employee'),
]
