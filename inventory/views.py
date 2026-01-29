from rest_framework import generics
from .models import Medicine
from .serializers import MedicineSerializer

class MedicineListCreateView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
