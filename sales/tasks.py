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
