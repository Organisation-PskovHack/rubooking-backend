from django.contrib import admin

from .models import (
    Hotel,
    UserHotel,
    Client, 
    UserClient,
    HotelNumber,
    Booking,
    Review
)

admin.site.register(HotelNumber)
admin.site.register(Booking)

