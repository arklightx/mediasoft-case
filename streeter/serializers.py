from rest_framework import serializers as sr
from .models import City, Street, Shop


class CitySerializer(sr.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class StreetSerializer(sr.ModelSerializer):
    city = CitySerializer(many=False, read_only=True)

    class Meta:
        model = Street
        fields = "__all__"


class ShopSerializer(sr.ModelSerializer):
    city = CitySerializer(many=False, read_only=True)
    street = StreetSerializer(many=False, read_only=True)

    class Meta:
        model = Shop
        fields = "__all__"
