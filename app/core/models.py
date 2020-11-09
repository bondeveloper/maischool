from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
                                    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email=None, password=None, **extra_fields):

        if not email or not password:
            raise ValueError("Email / Password cannot be empty.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        superuser = self.create_user(email, password)
        superuser.is_superuser = True

        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=255, default='unknown')
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Category(models.Model):

    basename = models.CharField(unique=True, max_length=255)
    displayname = models.CharField(max_length=255)
