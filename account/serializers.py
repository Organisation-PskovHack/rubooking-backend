from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer

from .models import (
    Hotel,
    Client,
    HotelNumber,
    Review,
    Booking
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("password", "last_login", "date_joined",
                   "is_superuser", "is_staff", "is_active",
                   "groups", "user_permissions")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.type == User.Types.HOTEL:
            try:
                hotel = Hotel.objects.get(pk=instance.id)
            except Hotel.DoesNotExist:
                pass
            else:
                data.update(HotelSerializer(hotel).data)
        elif instance.type == User.Types.CLIENT:
            try:
                client = Client.objects.get(pk=instance.id)
            except Client.DoesNotExist:
                pass
            else:
                data.update(ClientSerializer(client).data)
        return data


class CreateUserSerializer(DjoserUserCreateSerializer):

    class Meta:
        model = User
        exclude = ("last_login", "date_joined",
                   "is_superuser", "is_staff", "is_active", 
                   "groups", "user_permissions")


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    middle_name = serializers.CharField(source="user.middle_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Client
        fields = "__all__"


class HotelNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelNumber
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = "__all__"


class TokenSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="user.id")
    auth_token = serializers.CharField(source="key")
    type = serializers.CharField(source="user.type")

    class Meta:
        model = Token
        fields = ("id", "auth_token", "type", "verification")
