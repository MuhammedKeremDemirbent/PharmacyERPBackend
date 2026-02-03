#Kullanıcılar databasede durması için (diğerlerinden farklı AbstractUser kullandım)

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    
    def __str__(self):
        return self.username
    


    