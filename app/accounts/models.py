from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

from art.models import Art

class UserManager(BaseUserManager):
    
    def create_user(self, phone):
        # if not phone:
        #     raise ValueError('فرمت به درستی وارد نشده است، لطفا از اعداد انگلیسی استفاده کنید')
        user = self.model(phone=phone)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone):
        user = self.create_user(phone=phone)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        


class User(AbstractBaseUser):
    
    objects = UserManager()
    
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True)
    
    favorite_arts = models.ManyToManyField(Art, related_name='favorited_by', blank=True
)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.phone


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    