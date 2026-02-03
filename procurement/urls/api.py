from django.urls import path
from procurement.views import ProcurementListCreateView, ProcurementDetailView

urlpatterns = [
    path('', ProcurementListCreateView.as_view(), name='procurement-list-create'),
    path('<int:pk>/', ProcurementDetailView.as_view(), name='procurement-detail'),
]
