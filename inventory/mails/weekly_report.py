from celery import shared_task

@shared_task
def send_weekly_report():
    """
    Haftalık rapor
    """
    print("Haftalık Rapor Hazırlanıyor (Zamanlanmış Görev)")
    print("Rapor Gönderildi")
