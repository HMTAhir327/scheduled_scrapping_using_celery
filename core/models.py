
import email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,PermissionsMixin , BaseUserManager
from django.core.exceptions import ValidationError
from datetime import datetime


genderC  = (('M', 'male'),('F','female'),('O','other'))

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValidationError('email is required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user



class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    # birthday = models.DateField(input_formats=['%e-%b-%Y'],default='1 Jan 1970')
    birthday = models.DateField(default='1970-01-01')
    location = models.CharField(max_length=100, default='London')
    permium = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    gender = models.CharField(max_length=5,choices=genderC,default='O')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def age(self):
        today = datetime.today()
        dob = datetime(self.birthday)
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

    # def full_clean(self):
    #     if self.age() < 18:
    #         raise ValidationError('You must be 18 or older to register')
