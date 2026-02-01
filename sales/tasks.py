from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Sum
from .models import Sale
from django.conf import settings

@shared_task
def send_daily_sales_report():

    today = timezone.now().date() #Bugünün tarihi
    

    total_revenue = Sale.objects.filter(created_at__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    subject = f"GÜNLÜK RAPOR: {today.strftime('%d.%m.%Y')}"
    message = f"""
    Sayın Yönetici,
    
    Demirbent Eczanesi Gün Sonu Raporu:
    --------------------------------
    Tarih: {today.strftime('%d.%m.%Y')}
    Toplam Ciro: {total_revenue} TL
    
    İyi çalışmalar dileriz.
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['keremdmrbnt03@gmail.com'],
        fail_silently=False,
    )
    
    return f"Günlük Rapor Gönderildi: {total_revenue} TL"

@shared_task
def send_sale_receipt_email(sale_id):
    try:
        sale = Sale.objects.get(id=sale_id)
    except Sale.DoesNotExist:
        return "Satış bulunamadı!"

    # Müşterisi maili varsa at
    if not sale.patient or not sale.patient.email:
        return f"Satış #{sale_id} için e-posta gönderilemedi (Müşteri yok veya maili yok)."


    # Satın alınan ilaçları listeleme
    items_list = ""
    for item in sale.items.all():
        items_list += f"- {item.medicine.name} ({item.quantity} Adet) : {item.price} TL\n"

    subject = f"E-Fatura: Satış #{sale.id}"
    message = f"""Sayın {sale.patient.first_name} {sale.patient.last_name},
Eczanemizden yapmış olduğunuz alışveriş detayları aşağıdadır:

{items_list}
--------------------------------
Toplam Tutar: {sale.total_amount} TL 

Sağlıklı günler dileriz.
Demirbent Eczanesi"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[sale.patient.email],
        fail_silently=False,
    )

    return f"Fatura maili gönderildi: {sale.patient.email}"
