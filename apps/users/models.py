import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class BaseClass(models.Model):
    # UUIDField is optimized for database storage compared to CharField
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, **extra_fields):
        if not phone:
            raise ValueError('The Phone Number must be set')
        user = self.model(phone=phone, **extra_fields)
        # We use set_unusable_password() because authentication is OTP-based
        user.set_unusable_password() 
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(phone, **extra_fields)

class User(BaseClass, AbstractBaseUser, PermissionsMixin):
    # Added max_length and unique=True (crucial for login)
    phone = models.CharField(max_length=15, unique=True, null=False, blank=False)
    
    # Made optional so the OTP view can auto-create the user without crashing
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    
    # Changed to is_active (PEP 8 naming convention) and defaulted to True
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    bio = models.TextField(max_length=200, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    # Add fields here if you want them required when creating a superuser via CLI
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.phone