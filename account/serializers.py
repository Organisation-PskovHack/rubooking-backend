from rest_framework import serializers
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
