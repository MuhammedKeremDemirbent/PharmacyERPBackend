from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0 # Boş satır gösterme

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_amount', 'created_at') # Listede görünecek sütunlar
    inlines = [SaleItemInline] # Satışın içine girince ürünleri de göster

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'medicine', 'quantity', 'price')
