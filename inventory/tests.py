from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from inventory.models import Medicine

class MedicineTests(APITestCase):
    def test_create_medicine(self):
        """
        Yeni bir ilaç oluşturulabiliyor mu testi.
        """
        url = reverse('medicine-list-create') # urls.py'daki name='medicine-list-create'
        data = {
            "name": "Parol",
            "expiry_date": "2025-12-31",
            "price": 50.00,
            "how_many": 100
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medicine.objects.count(), 1)
        self.assertEqual(Medicine.objects.get().name, 'Parol')

    def test_list_medicines(self):
        """
        İlaçları listeleme testi.
        """
        
        Medicine.objects.create(name="Aspirin", expiry_date="2026-01-01", price=10, how_many=50)
        
        url = reverse('medicine-list-create')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertTrue(len(response.data) >= 1)
