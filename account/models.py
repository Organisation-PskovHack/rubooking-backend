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
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

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


class HotelNumber(models.Model):
    hotel = models.ForeignKey(Hotel, verbose_name="Отель", on_delete=models.CASCADE, related_name="numbers")
    residents = models.PositiveIntegerField(verbose_name="Количество проживающих")
    beds = models.PositiveIntegerField(verbose_name="Количество спальных мест")
    terms = models.TextField(verbose_name="Условия проживания")
    cost = models.PositiveIntegerField(verbose_name="Стоимость")

    class Meta:
        verbose_name = "Номер отеля"
        verbose_name_plural = "Номера отеля"


class ClientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user__type=User.Types.CLIENT)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    phone = models.CharField(verbose_name="Номер телефона", max_length=255)
    birth_date = models.DateField(verbose_name="Дата рождения")
    citizenship = models.CharField(verbose_name="Гражданство", max_length=255)

    objects = ClientManager()

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Review(models.Model):
    user = models.ForeignKey(User, verbose_name="Клиент", on_delete=models.CASCADE, related_name="reviews")
    hotel = models.ForeignKey(Hotel, verbose_name="Отель", on_delete=models.CASCADE, related_name="reviews")
    rate = models.PositiveIntegerField(
        verbose_name="Оценка",
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)]
    )
    text = models.TextField(verbose_name="Текст отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Booking(models.Model):
    user = models.ForeignKey(User, verbose_name="Клиент", on_delete=models.CASCADE, related_name="bookings")
    hotel = models.ForeignKey(Hotel, verbose_name="Отель", on_delete=models.CASCADE, related_name="bookings")
    hotel_number = models.ForeignKey(HotelNumber, verbose_name="Номер отеля", on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField(verbose_name="Дата бронирования")
    verified = models.BooleanField(verbose_name="Подтверждено?", default=False)

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
