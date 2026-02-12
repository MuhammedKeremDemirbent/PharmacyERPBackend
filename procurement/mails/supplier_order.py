from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from procurement.models import Procurement

@shared_task
def send_supplier_order_email(supplier_id, order_items, custom_message=None, custom_subject=None):
    """
    Tedarikçiye sipariş veya mesaj gönderir.
    """
    try:
        supplier = Procurement.objects.get(id=supplier_id)
    except Procurement.DoesNotExist:
        return "Tedarikçi bulunamadı."
        
    if not supplier.email:
        return f"{supplier.name} için mail adresi kayıtlı değil."
        
    items_text = ""
    if order_items:
        items_text += "Sipariş Listesi:\n"
        for item in order_items:
            # item dict olabilir veya string olabilir
            # Eğer dict ise item.get('name'), değilse item
            name = item.get('name') if isinstance(item, dict) else item
            quantity = item.get('quantity', 1) if isinstance(item, dict) else 1
            items_text += f"- {name} : {quantity} Kutu\n"
            
    # Özel konu başlığı varsa kullan, yoksa standart
    subject = custom_subject if custom_subject else f"Sipariş Talebi - Demirbent Eczanesi"

    if custom_message:
        body_text = custom_message
    else:
        body_text = "Aşağıdaki ürünlerin tarafımıza en kısa sürede gönderilmesini rica ederiz."

    final_message = f"""Sayın {supplier.name} Yetkilisi,

{body_text}

{items_text}

Saygılarımızla,
Demirbent Eczanesi"""
    
    send_mail(
        subject=subject,
        message=final_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[supplier.email],
        fail_silently=False,
    )
    
    return f"Mail gönderildi: {supplier.email}"
