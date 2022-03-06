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


class HotelViewset(viewsets.GenericViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, IsHotel]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [CurrentUserOrAdmin]
        elif self.request.method == "POST":
            self.permission_classes = [CurrentUserOrAdmin]
        return super().get_permissions()

    def retrieve(self, request, pk):
        instanse = self.get_object()
        serializer = self.serializer_class(instanse)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(instance=request.user, data=data, partial=True)
        if not user_serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer.update(request.user, user_serializer.validated_data)
        serializer.save(user_id=request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        instanse = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(instanse, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(instanse, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            qs = self.get_queryset()
            page = self.paginate_queryset(qs)
        except Hotel.DoesNotExist:
            return Response("Отели не найдены", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=["GET", "POST"],
        url_path="numbers",
        url_name="numbers",
        serializer_class=HotelNumberSerializer
    )
    def numbers(self, request, pk=None):
        if request.method == "GET":
            numbers = HotelNumber.objects.filter(hotel_id=pk)
            serializer = self.serializer_class(numbers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            data = request.data.copy()
            data["hotel"] = request.user.id
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        url_path="bookings",
        url_name="bookings",
        serializer_class=BookingSerializer
    )
    def bookings(self, request, pk=None):
        bookings = Booking.objects.filter(hotel_id=pk)
        serializer = self.serializer_class(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["GET", "POST"],
        url_path="reviews",
        url_name="reviews",
        serializer_class=ReviewSerializer
    )
    def reviews(self, request, pk=None):
        if request.method == "GET":
            reviews = Review.objects.filter(hotel_id=pk)
            serializer = self.serializer_class(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            data = request.data.copy()
            data["hotel"] = pk
            data["user"] = request.user.id
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=False):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientViewset(viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, IsClient]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [CurrentUserOrAdmin]
        return super().get_permissions()

    def retrieve(self, request, pk):
        instanse = self.get_object()
        serializer = self.serializer_class(instanse)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(instance=request.user, data=data, partial=True)
        if not user_serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer.update(request.user, user_serializer.validated_data)
        serializer.save(user_id=request.user.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        instanse = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(instanse, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(instanse, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            qs = self.get_queryset()
            page = self.paginate_queryset(qs)
        except Hotel.DoesNotExist:
            return Response("Отели не найдены", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        url_path="reviews",
        url_name="reviews",
        serializer_class=ReviewSerializer
    )
    def reviews(self, request, pk=None):
        numbers = Review.objects.filter(user_id=pk)
        serializer = self.serializer_class(numbers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        url_path="bookings",
        url_name="bookings",
        serializer_class=BookingSerializer
    )
    def bookings(self, request, pk=None):
        bookings = Booking.objects.filter(user_id=pk)
        serializer = self.serializer_class(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

