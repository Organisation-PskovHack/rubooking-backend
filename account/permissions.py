from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsHotel(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.type == User.Types.HOTEL

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.id == obj.hotel.pk
