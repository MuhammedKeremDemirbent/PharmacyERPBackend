from django.urls import path
from patients.views import PatientListCreateView

urlpatterns = [
    path('', PatientListCreateView.as_view(), name='patient-list-create'),
]
