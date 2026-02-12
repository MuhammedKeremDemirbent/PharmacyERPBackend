#Maili SMTP ile Gönderme Kodu

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_password_reset_email(email, reset_link, user_first_name):
    """
    Şifre sıfırlama mailini asenkron olarak gönderir.
    """
    subject = "Eczane ERP - Şifre Sıfırlama Talebi"
    message = f"""
    Merhaba {user_first_name},

    Şifrenizi sıfırlamak için aşağıdaki linke tıklayın:
    {reset_link}

    Bu link 15 dakika geçerlidir.
    Eğer bu talebi siz yapmadıysanız, lütfen dikkate almayınız.
    """
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
        return f"Şifre sıfırlama maili gönderildi: {email}"
    except Exception as e:
        return f"Mail gönderilemedi: {str(e)}"


#Asenkron-celery Mantığı ile Yapıldı