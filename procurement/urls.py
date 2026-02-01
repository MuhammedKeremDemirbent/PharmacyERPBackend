from django.urls import path
from .views import ProcurementListCreateView, ProcurementDetailView, SupplierOrderView

urlpatterns = [
    path('', ProcurementListCreateView.as_view(), name='procurement-list-create'),
    path('<int:pk>/', ProcurementDetailView.as_view(), name='procurement-detail'),
    path('<int:pk>/send-order/', SupplierOrderView.as_view(), name='send-supplier-order'),
]
