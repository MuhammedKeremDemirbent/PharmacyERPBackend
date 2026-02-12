from django.urls import path
from accounts.views.registration import RegisterEmployeeView
from accounts.views.password_reset import ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path('register-employee/', RegisterEmployeeView.as_view(), name='register-employee'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]
