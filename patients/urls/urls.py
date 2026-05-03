from django.urls import path
from patients.views import PatientListCreateView, PatientExcelUploadView, PatientRetrieveUpdateDestroyView

urlpatterns = [
    path('', PatientListCreateView.as_view(), name='patient-list-create'),
    path('<int:pk>/', PatientRetrieveUpdateDestroyView.as_view(), name='patient-detail'), #DELETE İÇİN
    path('excel-upload/', PatientExcelUploadView.as_view(), name='patient-excel-upload'),
]
