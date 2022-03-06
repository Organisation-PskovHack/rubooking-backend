from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from djoser.permissions import CurrentUserOrAdmin

from .models import (
    Hotel,
    Client,
    HotelNumber,
    Review,
    Booking
)
from .serializers import (
    UserSerializer,
    HotelSerializer,
    ClientSerializer,
    HotelNumberSerializer,
    ReviewSerializer,
    BookingSerializer
)
from .permissions import (
    IsHotel,
    IsClient
)

User = get_user_model()

# Create your views here.
