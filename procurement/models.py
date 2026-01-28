#procurement/models.py tedarik için bir database oluşturuyoruz

from django.db import models

class Procurement(models.Model):

    name = models.CharField(max_length=100, verbose_name="Tedarikçi Adı")
    phone_number_proc = models.CharField(max_length=15, verbose_name="Telefon Numarası", blank=True, null=True)
    address_proc = models.TextField(verbose_name="Adres", blank=True, null=True)

    def __str__(self):
        return f"{self.name}"