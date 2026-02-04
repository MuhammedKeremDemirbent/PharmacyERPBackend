from django.urls import path
from sales.views import CheckoutView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
