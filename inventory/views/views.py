from rest_framework import generics
from inventory.models import Medicine
from inventory.serializers import MedicineSerializer
from rest_framework.permissions import AllowAny # Herkese izin ver
from django.utils.decorators import method_decorator #Cache Backend
from django.views.decorators.cache import cache_page

# @method_decorator(cache_page(60 * 1), name='dispatch') # CACHE'I KAPATTIK: Sonra açarım proje büyüyünce
class MedicineListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicineSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Medicine.objects.filter(is_active=True)

class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [AllowAny]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


#modelviewset kullanılacak apilerde