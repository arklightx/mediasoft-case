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


class ShopReturnSerializer(sr.ModelSerializer):
    city = CitySerializer(many=False, read_only=True)
    street = StreetSerializer(many=False, read_only=True)

    class Meta:
        model = Shop
        fields = "__all__"


class ShopSerializer(sr.ModelSerializer):
    city = sr.PrimaryKeyRelatedField(many=False, queryset=City.objects.all())
    street = sr.PrimaryKeyRelatedField(many=False, queryset=Street.objects.all())

    def save(self, **kwargs):
        city = kwargs.get("city")
        street = kwargs.get("street")
        if city and street:
            if city.id != street.city.id:
                raise Exception("ID города не совпадает с ID города улицы")
        return super().save(**kwargs)

    def update(self, instance, validated_data):
        city = validated_data.get("city")
        street = validated_data.get("street")
        if city and street:
            if city.id != street.city.id:
                raise Exception("ID города не совпадает с ID города улицы")
            return super().update(instance, validated_data)
        if street:
            if instance.city.id != street.city.id:
                raise Exception("ID города не совпадает с ID города улицы")
        return super().update(instance, validated_data)

    class Meta:
        model = Shop
        fields = "__all__"
