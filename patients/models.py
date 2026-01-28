#patients/models.py hastalar(müşteriler) için bir database oluşturuyoruz

from django.db import models

class Patient(models.Model):

    first_name = models.CharField(max_length=100, verbose_name="Ad")
    last_name = models.CharField(max_length=100, verbose_name="Soyad")
    phone_number = models.CharField(max_length=15, verbose_name="Telefon Numarası", blank=True, null=True)
    address = models.TextField(verbose_name="Adres", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"