from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have an username address")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(blank=True,null=True)

    objects = CustomUserManager()
    
    class Meta:
        ordering = ["email"]
    
    def __str__(self):
        return self.username