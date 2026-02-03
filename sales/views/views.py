from rest_framework import generics
from sales.models import Sale
from sales.serializers import SaleSerializer
from sales.views.checkout import CheckoutView

class SaleListView(generics.ListAPIView):
    queryset = Sale.objects.all().order_by('-created_at')
    serializer_class = SaleSerializer

class SaleDetailView(generics.RetrieveDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
