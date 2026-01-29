from rest_framework import generics
from .models import Procurement
from .serializers import ProcurementSerializer

class ProcurementListCreateView(generics.ListCreateAPIView):
    queryset = Procurement.objects.all()
    serializer_class = ProcurementSerializer
