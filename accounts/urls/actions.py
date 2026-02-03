from django.urls import path
from accounts.views import RegisterEmployeeView

urlpatterns = [
    path('register-employee/', RegisterEmployeeView.as_view(), name='register-employee'),
]
