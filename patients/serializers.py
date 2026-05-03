from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'tc', 'first_name', 'last_name', 'phone_number', 'email', 'address', 'created_at']
