from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .models import Sale, SaleItem
from inventory.models import Medicine
from .serializers import CheckoutSerializer

class CheckoutView(APIView):
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        items_data = serializer.validated_data['items']
        
        # ATOMIC TRANSACTION (Ya hepsi olur, ya hiçbiri olmaz)
        # Eğer stok düşerken hata olursa, satışı da iptal eder.
        with transaction.atomic():
            # 1. Satış Kaydı Oluştur
            sale = Sale.objects.create()
            total_price = 0

            for item in items_data:
                product_id = item['product_id']
                quantity = item['quantity']

                try:
                    # Kilitleme (select_for_update): Aynı anda başkası alamasın
                    medicine = Medicine.objects.select_for_update().get(id=product_id)
                except Medicine.DoesNotExist:
                    return Response({"error": f"Ürün bulunamadı ID: {product_id}"}, status=status.HTTP_404_NOT_FOUND)

                # 2. Stok Kontrolü
                if medicine.how_many < quantity:
                    return Response(
                        {"error": f"{medicine.name} stoğu yetersiz! (Kalan: {medicine.how_many})"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # 3. Stoktan Düş
                medicine.how_many -= quantity
                medicine.save()

                # 4. Satış Detayı Ekle
                SaleItem.objects.create(
                    sale=sale,
                    medicine=medicine,
                    quantity=quantity,
                    price=medicine.price # O anki fiyatı kaydet
                )
                
                total_price += medicine.price * quantity

            # Toplam tutarı güncelle
            sale.total_amount = total_price
            sale.save()

        return Response(
            {"message": "Satış Başarılı!", "sale_id": sale.id, "total": total_price}, 
            status=status.HTTP_201_CREATED
        )
