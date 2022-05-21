from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StreetViewSet, StreetByCityView, ShopViewSet, CityViewSet

router = DefaultRouter()
router.register("city", CityViewSet)
router.register("street", StreetViewSet)
router.register("shop", ShopViewSet)

urlpatterns = [
    path("city/<int:id>/street/", StreetByCityView.as_view())
] + router.urls
