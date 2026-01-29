from django.urls import path
from .views import ProcurementListCreateView, ProcurementDetailView, SendEmailToSupplierView

urlpatterns = [
    path('', ProcurementListCreateView.as_view(), name='procurement-list-create'),
    path('<int:pk>/', ProcurementDetailView.as_view(), name='procurement-detail'),
    path('<int:pk>/send-email/', SendEmailToSupplierView.as_view(), name='send-email-to-supplier'),
]
