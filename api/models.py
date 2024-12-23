from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Hobby(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        raise NotImplementedError("This application does not support superusers.")


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    is_active = models.BooleanField(default=True)  # Allows user accounts to be deactivated

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email
