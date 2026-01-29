from django.urls import path
from .views import MedicineListCreateView

urlpatterns = [
    path('medicines/', MedicineListCreateView.as_view(), name='medicine-list-create'),
]
