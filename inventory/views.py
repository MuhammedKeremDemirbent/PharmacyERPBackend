from rest_framework import generics
from .models import Medicine
from .serializers import MedicineSerializer
from rest_framework.permissions import AllowAny # Herkese izin ver

class MedicineListCreateView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [AllowAny]

class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [AllowAny]
