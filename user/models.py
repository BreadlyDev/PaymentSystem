from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=150, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.email}'

    def save(self, *args, **kwargs):
        if self.password and not str(self.password).startswith(('pbkdf2_sha256$', 'bcrypt')):
            self.set_password(self.password)
        super().save(*args, **kwargs)


# class Account(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account')
#     number = models.CharField(max_length=200)
#
#     class Meta:
#         db_table = 'accounts'
#         verbose_name = 'Счет'
#         verbose_name_plural = 'Счета'
#
#     def __str__(self):
#         return f'Счет'
#
#
# class Card(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account')
#     number = models.CharField(max_length=200)
#     expiration = models.DateField()
#     cvv = models.CharField(max_length=200)
#
#     class Meta:
#         db_table = 'card'
#         verbose_name = 'Банковская карта'
#         verbose_name_plural = 'Банковские карты'
#
#     def __str__(self):
#         return f'Карта'
