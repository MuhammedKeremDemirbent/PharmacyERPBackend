from django.urls import path
from inventory.views import MedicineListCreateView, MedicineDetailView, MedicineExcelUploadView

urlpatterns = [
    path('medicines/', MedicineListCreateView.as_view(), name='medicine-list-create'),
    path('medicines/excel-upload/', MedicineExcelUploadView.as_view(), name='medicine-excel-upload'),
    path('medicines/<int:pk>/', MedicineDetailView.as_view(), name='medicine-detail'), #DELETE İÇİN
]
