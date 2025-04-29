from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

NULLABLE = {'blank': True, 'null': True}


class UserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    username = None

    phone = models.CharField(max_length=255, unique=True, verbose_name='Номер телефона', **NULLABLE)
    first_name = models.CharField(max_length=255, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=255, verbose_name='Фамилия', **NULLABLE)
    country = models.CharField(max_length=255, verbose_name='Страна')
    email = models.EmailField(unique=True, verbose_name='Почта')
    token = models.CharField(max_length=255, verbose_name='Token', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='avatar', **NULLABLE)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            (
                'view_user_list',
                'Can view user list'
            ),
            (
                'block_user',
                'Can block users'
            ),
        ]

    def __str__(self):
        return f'{self.email}, {self.first_name}, {self.last_name}'
