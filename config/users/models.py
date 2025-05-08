# models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class UserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        # Добавляем обязательные поля для суперпользователя
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('country', 'Unknown')  # Укажите значение по умолчанию

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    username = None  # Полностью отключаем username
    phone = models.CharField(max_length=20, unique=True, verbose_name='Телефон', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='Страна', default='Unknown')  # Значение по умолчанию
    email = models.EmailField(unique=True, verbose_name='Email')
    token = models.CharField(max_length=255, **NULLABLE)
    avatar = models.ImageField(upload_to='users/', **NULLABLE)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Поля для createsuperuser (email уже учтен)

    def __str__(self):
        return self.email


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='community_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_company = models.BooleanField(default=False)

    # Дополнительные поля при необходимости

    def __str__(self):
        return self.user.username