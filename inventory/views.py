from rest_framework import generics
from .models import Medicine
from .serializers import MedicineSerializer
from rest_framework.permissions import AllowAny # Herkese izin ver
from django.utils.decorators import method_decorator #Cache Backend
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 1), name='dispatch') #Veritabanını yormaz
class MedicineListCreateView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [AllowAny]

class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [AllowAny]
