#Inventory/models.py içinde ilaçların bilgilerini tutuyoruz
from django.db import models

class Medicine(models.Model):
   
    FORM_TYPE = [
        ('TABLET', 'Hap / Tablet'),
        ('LIQUID', 'Sıvı / Şurup'),
        ('OTHER', 'Diğer'),
    ]

    barcode = models.CharField(max_length=13, verbose_name="Barkod", unique=True, null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="İlaç Adı")
    expiry_date = models.DateField(verbose_name="Son Kullanma Tarihi")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")
    form_type = models.CharField(max_length=10, choices=FORM_TYPE, default='TABLET', verbose_name="Hap mı Sıvı mı?")
    how_many = models.IntegerField(default=0, verbose_name="Stok Adedi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    supplier = models.ForeignKey('procurement.Procurement', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tedarikçi") # Yeni Bağlantı

    def __str__(self):
        return self.name   
