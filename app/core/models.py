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

    USERNAME_FIELD = EMAIL_FIELD = 'email'


class Category(models.Model):

    basename = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)


class School(models.Model):

    basename = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,
                                 blank=True, null=True
                                 )
    users = models.ManyToManyField(get_user_model(), through='Profile')


class Profile(models.Model):
    user = models.ForeignKey(get_user_model(),  on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'school'),)


class Subject(models.Model):
    basename = models.CharField(unique=True, max_length=255)
    name = models.CharField(unique=True, max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


class Level(models.Model):
    basename = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING,
                               blank=True, null=True
                               )


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.DO_NOTHING)
    instructor = models.ForeignKey(get_user_model(),
                                   related_name="instructor",
                                   on_delete=models.DO_NOTHING
                                   )
    learners = models.ManyToManyField(get_user_model(), blank=True,
                                      related_name="learners")
    name = models.CharField(max_length=255)


class Session(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    type = models.CharField(
                            max_length=50,
                            choices=[
                                ('LCT', "Lecture"),
                                ('TST', "Test"),
                                ('XM', "Exam"),
                                ('TCN', "Teaching"),
                                ('PRT', "Practical")
                            ],
                            default='Teaching'
                            )
    attendance = models.ManyToManyField(get_user_model(), blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class Attachment(models.Model):
    notes = models.CharField(max_length=255)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    file = models.FileField(upload_to='session')


class Moderation(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    learner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    learner_score = models.IntegerField()
    max_score = models.IntegerField()
    score_type = models.CharField(
                                  max_length=20,
                                  choices=[
                                    ('unit', 'Unit'),
                                    ('percentage', 'Percentage')
                                  ],
                                  default='units'
                                  )
