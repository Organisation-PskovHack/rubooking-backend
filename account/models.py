from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser, BaseUserManager

from .managers import UserManager

class User(AbstractUser):
    class Types(models.TextChoices):
        HOTEL = "HOTEL", "Отель"
        CLIENT = "CLIENT", "Клиент"

    username = None
    email = models.EmailField(
        "Email адрес",
        unique=True,
        validators=[validators.validate_email],
        error_messages={
            "unique": "Пользователь с таким email уже существует.",
        },
    )
    type = models.CharField(verbose_name="Тип", max_length=50, choices=Types.choices)

    first_name = models.CharField(verbose_name="Имя", max_length=100)
    last_name = models.CharField(verbose_name="Фамилия", max_length=100)
    middle_name = models.CharField(verbose_name="Отчество", max_length=100, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()

    objects = UserManager()

# Create your models here.
