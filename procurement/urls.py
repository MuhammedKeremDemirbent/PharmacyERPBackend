from django.urls import path
from .views import ProcurementListCreateView

urlpatterns = [
    path('', ProcurementListCreateView.as_view(), name='procurement-list-create'),
]
