from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import User

@shared_task
def send_welcome_email(user_id, password):
    """
    Yeni kayıt olan personel için hoşgeldin maili (RegisterEmployeeView için).
    """
    try:
        user = User.objects.get(id=user_id)
        subject = "Eczane ERP Sistemine Hoşgeldiniz!"
        message = f"""
        Merhaba {user.first_name},
        
        Eczane ERP sistemine personel kaydınız yapılmıştır.
        Giriş Bilgileriniz:
        
        Kullanıcı Adı: {user.username}
        Şifre: {password}
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        return f"Hoşgeldin maili gönderildi: {user.email}"
    except User.DoesNotExist:
        return f"Kullanıcı bulunamadı: {user_id}"
    except Exception as e:
        return f"Mail hatası: {str(e)}"
