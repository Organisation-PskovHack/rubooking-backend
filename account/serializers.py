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
