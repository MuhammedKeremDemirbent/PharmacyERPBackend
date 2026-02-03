from rest_framework import generics
from procurement.models import Procurement
from procurement.serializers import ProcurementSerializer
from procurement.views.proc_mails import SupplierOrderView

class ProcurementListCreateView(generics.ListCreateAPIView):
    queryset = Procurement.objects.all()
    serializer_class = ProcurementSerializer

class ProcurementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Procurement.objects.all()
    serializer_class = ProcurementSerializer