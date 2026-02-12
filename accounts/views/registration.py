from accounts.serializers import RegisterEmployeeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAdminUser

# Kullanıcı (adminler) Oluşturma Mailpit ile Mail Atma(Celery)  
class RegisterEmployeeView(APIView):
    permission_classes = [IsAdminUser] # Sadece Adminler personel ekleyebilir

    def post(self, request):
        serializer = RegisterEmployeeSerializer(data=request.data)
        
        if serializer.is_valid():
            # Rastgele şifre üretiriz
            random_password = get_random_string(length=8)
            
            # Kullanıcıyı kaydederiz şifreyi hashleriz
            user = serializer.save()
            user.set_password(random_password)
            user.save()
            
            # E-Posta Gönderme Kısmı (Celery - apply_async ile)
            from accounts.tasks import send_welcome_email
            send_welcome_email.apply_async(args=[user.id, random_password])

            return Response({
                "message": f"Personel {user.username} oluşturuldu. E-posta kuyruğa eklendi.",
                "generated_password": random_password 
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
