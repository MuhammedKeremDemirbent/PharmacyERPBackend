from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from sales.models import Sale
from core.idempotent.mail_idempotent import mail_idempotent #idempotency

@shared_task(bind=True) # bind=True önemli, self argümanı için
@mail_idempotent(expire=60*60*24) # 24 saat koruma
def send_sale_receipt_email(self, sale_id):
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
