from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import User
from .serializers import UserSerializer, RegisterEmployeeSerializer

# Kullanıcı Listeleme ve Oluşturma Mailpit ile Mail Atma(Celery)      
  
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
            
            # E-Posta Gönderme Kısmı
            subject = "Eczane ERP Sistemine Hoşgeldiniz!"
            message = f"""
            Merhaba {user.first_name},
            
            Eczane ERP sistemine personel kaydınız yapılmıştır.
            Giriş Bilgileriniz:
            
            Kullanıcı Adı: {user.username}
            Şifre: {random_password}
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                email_status = "E-posta gönderildi."
            except Exception as e:
                email_status = f"E-posta gönderilemedi: {str(e)}"

            return Response({
                "message": f"Personel {user.username} oluşturuldu. {email_status}",
                "generated_password": random_password 
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
