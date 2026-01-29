from celery import shared_task
from django.core.mail import send_mail
import time

@shared_task
def check_stock_metrics():
    """
    Bu görev Celery Worker tarafından arka planda çalıştırılacak.
    (Simülasyon: Stok kontrolü yapıp rapor atıyor gibi davranır)
    """
    print("Stok Kontrolü Başladı")
    time.sleep(5) # Uzun süren bir işlemi simüle ediyoruz
    print("Stok Kontrolü Bitti")
    return "Kontrol Tamamlandı"

@shared_task
def send_weekly_report():
    """
    Bu görev Celery Beat tarafından zamanlanmış olarak çalıştırılacak.
    """
    print("Haftalık Rapor Hazırlanıyor")
    #mail atma kodu 
    print("Rapor Gönderildi")

