from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from .models import Procurement
from .serializers import ProcurementSerializer

class ProcurementListCreateView(generics.ListCreateAPIView):
    queryset = Procurement.objects.all()
    serializer_class = ProcurementSerializer

class ProcurementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Procurement.objects.all()
    serializer_class = ProcurementSerializer

from django.conf import settings

class SendEmailToSupplierView(APIView):
    def post(self, request, pk):
        try:
            supplier = Procurement.objects.get(pk=pk)
        except Procurement.DoesNotExist:
            return Response({"error": "Tedarikçi bulunamadı"}, status=status.HTTP_404_NOT_FOUND)

        if not supplier.email:
            return Response({"error": "Bu tedarikçinin e-posta adresi yok!"}, status=status.HTTP_400_BAD_REQUEST)

        # Frontend'den gelen mesajı alamazsak varsayılan bir mesaj atar
        subject = request.data.get('subject', 'Eczane Sipariş Talebi')
        message = request.data.get('message', f'Merhaba {supplier.name}, sipariş geçmek istiyoruz.')

        sent_count = send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL, # Dinamik gönderici adresi
            [supplier.email],
            fail_silently=False,
        )

        if sent_count > 0:
             return Response({"message": f"E-posta başarıyla gönderildi: {supplier.email}"}, status=status.HTTP_200_OK)
        else:
             return Response({"error": "E-posta gönderilemedi"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)