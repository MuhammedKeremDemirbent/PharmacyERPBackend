from rest_framework import serializers
from .models import Sale, SaleItem

class SaleItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField() # Frontend 'product_id' yolluyor
    quantity = serializers.IntegerField()

    class Meta:
        model = SaleItem
        fields = ['product_id', 'quantity']

class CheckoutSerializer(serializers.Serializer):
    items = SaleItemSerializer(many=True)
    patient_id = serializers.IntegerField(required=False, allow_null=True) # Müşteri ID opsiyonel
