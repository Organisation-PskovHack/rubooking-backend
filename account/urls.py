from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"hotels", HotelViewset, basename="hotels")
router.register(r"clients", ClientViewset, basename="clients")
router.register(r"bookings", BookingViewset, basename="bookings")

urlpatterns = [
] + router.urls
