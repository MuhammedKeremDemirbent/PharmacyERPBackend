from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import User
from .serializers import UserSerializer, RegisterEmployeeSerializer

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterEmployeeView(APIView):
    permission_classes = [IsAdminUser] # Sadece Adminler personel ekleyebilir

    def post(self, request):
        serializer = RegisterEmployeeSerializer(data=request.data)
        
        if serializer.is_valid():
            # 1. Rastgele Şifre Üret (8 karakter)
            random_password = get_random_string(length=8)
            
            # 2. Kullanıcıyı Kaydet (Şifreyi Hashle)
            user = serializer.save()
            user.set_password(random_password)
            user.save()
            
            # 3. E-Posta Gönder (Açık şifreyi)
            subject = "Eczane ERP Sistemine Hoşgeldiniz"
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
