from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import (
    Hotel,
    Client,
    HotelNumber,
    Review,
    Booking
)

class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name")
    first_name = serializers.CharField(source="user.first_name")
    middle_name = serializers.CharField(source="user.middle_name")
    email = serializers.EmailField(source="user.email")

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
