from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self,  **extra_fields):
        email = extra_fields.pop("email")
        password = extra_fields.pop("password")
        role = extra_fields.pop("role")
        if not email:
            raise ValueError("Email is mandatory")

        if not password:
            raise ValueError("Password is mandatory")
        if not role:
            raise ValueError("role is mandatory")

        extra_fields.setdefault('is_active', True)
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, ** extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Profile(models.Model):
    profile_picture = models.ImageField(
        upload_to="profiles/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")


class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("moderator", "Moderator"),
        ("user", "User"),
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(
        max_length=30, choices=ROLE_CHOICES)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email
