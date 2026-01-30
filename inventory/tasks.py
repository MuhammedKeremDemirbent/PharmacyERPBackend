# Celery ile görevler oluşturuyoruz ve logluyoruz

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Medicine

@shared_task
def check_stock_metrics():
    """
    10'dan az kalan ilaçları raporlar ve mail atar.
    """
    print("Stok Kontrolü Başladı")
    
    # 10'dan az ise
    low_stock_medicines = Medicine.objects.filter(how_many__lt=10)
    
    if low_stock_medicines.exists():
        count = low_stock_medicines.count()
        print(f"DİKKAT! {count} adet ilaç kritik seviyede:")
        
        # Mail İçeriği Hazırla
        message_body = f"DİKKAT! {count} adet ilaç stokta azalmıştır.\n\nEksik İlaçlar:\n"
        for med in low_stock_medicines:
            line = f"- {med.name} (Kalan: {med.how_many})"
            print(line)
            message_body += line + "\n"
            
        message_body += "\nLütfen tedarik işlemlerini başlatınız."

        # Mailpit yerine ilerde Mailgun veya AWS
        send_mail(
            subject="ACİL: Kritik Stok Uyarısı",
            message=message_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['keremdmrbnt03@gmail.com'],
            fail_silently=False,
        ) 
        return f"Mail Gönderildi: {count} ilaç eksik."
        
    else:
        print("Stok durumu harika! Eksik ilaç yok.")
        
    return "Kontrol Tamamlandı (Sorun Yok)"

@shared_task
def send_weekly_report():
    """
    Haftalık rapor
    """
    print("Haftalık Rapor Hazırlanıyor (Zamanlanmış Görev)")
    print("Rapor Gönderildi")
