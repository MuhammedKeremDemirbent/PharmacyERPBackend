from celery import shared_task
from django.core.mail import send_mass_mail
from .models import Patient
from django.conf import settings

@shared_task
def send_weekly_campaign_email():
    # E-Postası olan tüm hastalar
    patients = Patient.objects.exclude(email__isnull=True).exclude(email__exact='')
        
    messages = []
    subject = "Sağlıklı Haftalar Dileriz!"
    
    for patient in patients:
        text = f"""
        Sayın {patient.first_name} {patient.last_name},
        
        Mutlu ve sağlıklı bir hafta geçirmenizi dileriz.
        İlaçlarınızın takibini yapmayı unutmayın!
        
        Saygılarımızla,
        Demirbent Eczanesi
        """
        
        messages.append((subject, text, settings.DEFAULT_FROM_EMAIL, [patient.email]))
    
    if messages:
        send_mass_mail(tuple(messages), fail_silently=False)
        return f"{len(messages)} kişiye haftalık mail gönderildi."
    else:
        return "Gönderilecek kimse bulunamadı."
