from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    phone = models.CharField(max_length=255, unique=True, verbose_name='Номер телефона', **NULLABLE)
    first_name = models.CharField(max_length=255, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=255, verbose_name='Фамилия', **NULLABLE)
    country = models.CharField(max_length=255, verbose_name='Страна')
    email = models.EmailField(unique=True, verbose_name='Почта')
    token = models.CharField(max_length=255, verbose_name='Token', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='avatar', **NULLABLE)

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

