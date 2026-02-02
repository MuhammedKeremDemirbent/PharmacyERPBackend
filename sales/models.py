from django.db import models
from inventory.models import Medicine  # İlaçları buradan çekeceğiz

from django.conf import settings # User modeli için gerekli
from patients.models import Patient # Hastayı bağlamak için gerekli

from django.utils import timezone

# SATIŞ İŞLEMİ 
class Sale(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Satışı Yapan Personel")
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Müşteri") # CRM Bağı
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Satış Tarihi")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Toplam Tutar")

    def __str__(self):
        local_time = timezone.localtime(self.created_at)
        return f"Satış #{self.id} - {local_time.strftime('%d.%m.%Y %H:%M')}"

# SATIŞ DETAYI
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, verbose_name="Satılan İlaç")
    quantity = models.IntegerField(default=1, verbose_name="Adet")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Satış Fiyatı")

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity}"