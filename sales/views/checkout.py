from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from sales.models import Sale, SaleItem
from inventory.models import Medicine
from sales.serializers import CheckoutSerializer
from django.utils.decorators import method_decorator
from core.idempotent.view_idempotent import idempotent

class CheckoutView(APIView):
    
    @method_decorator(idempotent(timeout=300), name='post') #Idempotency 300 saniye
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        items_data = serializer.validated_data['items']
        patient_id = serializer.validated_data.get('patient_id') 
        
       
        with transaction.atomic():
            # Satışı yapan kişiyi ve varsa Müşteriyi kaydetme
            user = request.user if request.user.is_authenticated else None
            sale = Sale.objects.create(user=user, patient_id=patient_id)
            total_price = 0
            
            for item in items_data:
                product_id = item['product_id']
                quantity = item['quantity']

                try:
                    medicine = Medicine.objects.select_for_update().get(id=product_id)
                except Medicine.DoesNotExist:
                    return Response({"error": f"Ürün bulunamadı ID: {product_id}"}, status=status.HTTP_404_NOT_FOUND)

                if medicine.how_many < quantity:
                    return Response(
                        {"error": f"{medicine.name} stoğu yetersiz! (Kalan: {medicine.how_many})"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

                medicine.how_many -= quantity
                medicine.save()

                SaleItem.objects.create(
                    sale=sale,
                    medicine=medicine,
                    quantity=quantity,
                    price=medicine.price # O anki fiyat
                )
                
                total_price += medicine.price * quantity

            # Toplam tutarı güncelleme
            sale.total_amount = total_price
            sale.save()

        # Fatura Mailini Kuyruğa Atma
        try:
            from sales.tasks import send_sale_receipt_email
            # apply_async, countdown=2 saniye gecikmeli
            send_sale_receipt_email.apply_async(args=[sale.id], countdown=2)
        except Exception as e:
            print(f"Mail kuyruğa eklenemedi: {e}")

        return Response(
            {"message": "Satış Başarılı!", "sale_id": sale.id, "total": total_price}, 
            status=status.HTTP_201_CREATED
        )
