from celery import shared_task

from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count
from django.core.mail import send_mail
from django.conf import settings
from inventory.models import Medicine
from sales.models import Sale, SaleItem

@shared_task
def send_weekly_report():
    """
    Haftalık Satış ve Stok Raporunu Hazırlar ve Gönderir.
    """
    print("📊 Haftalık Rapor Hazırlanıyor...")
    
    #Tarih Aralığı 1 hafta
    today = timezone.now()
    last_week = today - timedelta(days=7)
    
    #Haftalık Satış Verileri
    weekly_sales = Sale.objects.filter(created_at__gte=last_week)
    total_revenue = weekly_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_orders = weekly_sales.count()
    
    #Kritik Stoklar
    low_stock_count = Medicine.objects.filter(how_many__lt=10).count()
    
    # 4. En Çok Satan 3 İlaç (Opsiyonel ama şık durur)
    top_items = SaleItem.objects.filter(sale__created_at__gte=last_week)\
        .values('medicine__name')\
        .annotate(total_qty=Sum('quantity'))\
        .order_by('-total_qty')[:3]

    # Mail İçeriği Oluşturma
    message = f"""
    Sayın Yönetici,
    
    İşte eczanenizin haftalık performans raporu ({last_week.strftime('%d.%m')} - {today.strftime('%d.%m')}):
    
    💰 Finansal Durum:
    ------------------
    Toplam Ciro: {total_revenue:,.2f} TL
    Toplam Satış Adedi: {total_orders}
    
    📦 Stok Durumu:
    ------------------
    Kritik Seviyedeki İlaç Sayısı: {low_stock_count}
    
    🏆 Haftanın Yıldızları (En Çok Satanlar):
    ------------------
    """
    
    for item in top_items:
        message += f"- {item['medicine__name']}: {item['total_qty']} adet\n"
        
    message += "\nİyi haftalar dileriz.\nPharmacy ERP Sistemi"

    # Maili Gönder
    send_mail(
        subject=f"Haftalık Rapor: {today.strftime('%d.%m.%Y')}",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['[EMAIL_ADDRESS]'], # Burayı kendi mailiniz yapabilirsiniz
        fail_silently=False,
    )
    
    return f"Haftalık Rapor Gönderildi. Ciro: {total_revenue} TL"
