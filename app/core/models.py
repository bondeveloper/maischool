from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
                                    PermissionsMixin
from django.contrib.auth import get_user_model


class UserManager(BaseUserManager):

    def create_user(self, email=None, password=None, **extra_fields):

        if not email or not password:
            raise ValueError("Please fill in all the required fields.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        superuser = self.create_user(email, password, **extra_fields)
        superuser.is_superuser = True

        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Category(models.Model):

    basename = models.CharField(unique=True, max_length=255)
    displayname = models.CharField(max_length=255)


class School(models.Model):

    basename = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,
                                 blank=True, null=True)
    users = models.ManyToManyField(get_user_model(), through='Profile')


class Profile(models.Model):
    user = models.ForeignKey(get_user_model(),  on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'school'),)
