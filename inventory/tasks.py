# Celery ile görevler oluşturuyoruz ve logluyoruz

from celery import shared_task
from .models import Medicine

@shared_task
def check_stock_metrics():
    """
    10'dan az kalan ilaçları raporlar.
    """
    print("Stok Kontrolü Başladı")
    
    #10'dan az ise mesaj gitsin
    low_stock_medicines = Medicine.objects.filter(how_many__lt=10)
    
    if low_stock_medicines.exists():
        print(f"DİKKAT! {low_stock_medicines.count()} adet ilaç kritik seviyede:")
        for med in low_stock_medicines:
            print(f" - {med.name} (Kalan: {med.how_many})")
            
        # 'send_mail' ekleyeceğiz eczacıya mail gidecek
    else:
        print("Stok durumu harika! Eksik ilaç yok.")
        
    return "Kontrol Tamamlandı"

@shared_task
def send_weekly_report():
    """
    Haftalık rapor
    """
    print("Haftalık Rapor Hazırlanıyor (Zamanlanmış Görev)")
    # Burada normalde mail atma kodu olur şuan yok
    print("Rapor Gönderildi")
