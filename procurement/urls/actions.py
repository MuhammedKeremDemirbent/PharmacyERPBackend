from django.urls import path
from procurement.views import SupplierOrderView

urlpatterns = [
    path('<int:pk>/send-order/', SupplierOrderView.as_view(), name='send-supplier-order'),
]
