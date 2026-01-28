from rest_framework import serializers
from .models import Procurement

class ProcurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procurement
        fields = ['id', 'name', 'phone_number_proc', 'address_proc']
