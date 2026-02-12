from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from procurement.models import Procurement

class SupplierOrderView(APIView):
    def post(self, request, pk):
        try:
            supplier = Procurement.objects.get(pk=pk)
        except Procurement.DoesNotExist:
            return Response({"error": "Tedarikçi bulunamadı"}, status=status.HTTP_404_NOT_FOUND)

        # Frontend: {"items": [{"name": "Parol", "quantity": 10}]} OR {"message": "..."}
        order_items = request.data.get('items', [])
        message = request.data.get('message', '')
        subject = request.data.get('subject', '')

        if not order_items and not message:
             return Response({"error": "Sipariş listesi veya mesaj boş olamaz!"}, status=status.HTTP_400_BAD_REQUEST)

        # Celery Task (Async - apply_async ile)
        from procurement.tasks import send_supplier_order_email
        send_supplier_order_email.apply_async(
            args=[supplier.id, order_items], 
            kwargs={'custom_message': message, 'custom_subject': subject}
        )

        return Response({"message": f"Sipariş talebi alındı, e-posta gönderiliyor: {supplier.email}"}, status=status.HTTP_200_OK)