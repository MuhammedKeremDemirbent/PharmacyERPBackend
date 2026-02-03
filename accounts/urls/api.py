from django.urls import path
from accounts.views import UserListCreateView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list'),
]
