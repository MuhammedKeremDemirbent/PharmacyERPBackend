from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from sales.models.models import Sale
from sales.mails.pdf_creator import generate_sale_receipt_pdf
from core.idempotent.mail_idempotent import mail_idempotent

@shared_task(bind=True) # bind=True önemli, self argümanı için
@mail_idempotent(expire=60*60*24) # 24 saat koruma
def send_sale_receipt_email(self, sale_id):
    try:
        sale = Sale.objects.get(id=sale_id)
    except Sale.DoesNotExist:
        return "Satış bulunamadı!"

    # Müşterisi maili varsa at
    if not sale.patient:
        print(f"📧 Satış #{sale_id} için Müşteri bulunamadı. İptal.")
        return f"Satış #{sale_id} için e-posta gönderilemedi (Müşteri yok)."
    
    if not sale.patient.email:
        print(f"📧 Satış #{sale_id} için Müşteri email adresi yok. İptal.")
        return f"Satış #{sale_id} için e-posta gönderilemedi (Mail adresi yok)."

    print(f"📧 Satış #{sale_id} için mail gönderiliyor: {sale.patient.email}")


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

    # PDF Oluştur
    pdf_buffer = generate_sale_receipt_pdf(sale_id)

    # EmailMessage Nesnesi Oluştur
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[sale.patient.email],
    )

    # PDF'i Ekle
    email.attach(f"ECZANE_FIS_{sale.id}.pdf", pdf_buffer.getvalue(), 'application/pdf')

    # Gönder
    email.send(fail_silently=False)

    return f"Fatura maili (PDF ekli) gönderildi: {sale.patient.email}"
