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


class HotelManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user__type=User.Types.HOTEL)


class Hotel(models.Model):
    title = models.CharField(verbose_name="Название", max_length=255)
    image = models.ImageField(verbose_name="Фото")
    address = models.TextField(verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание")
    terms = models.TextField(verbose_name="Условия проживания")
    rate = models.PositiveIntegerField(verbose_name="Рейтинг")

    objects = HotelManager()

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"
