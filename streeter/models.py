from datetime import timedelta, time, datetime

from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название города")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}. {self.name}"


class Street(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название улицы")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.city} -> {self.name}"


class Shop(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название магазина")
    house = models.CharField(max_length=10, verbose_name="Дом")
    open_time = models.TimeField(verbose_name="Время открытия")
    close_time = models.TimeField(verbose_name="Время закрытия")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город")
    street = models.ForeignKey(Street, on_delete=models.SET_NULL, null=True, verbose_name="Улица")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.id}. {self.city.name} -> {self.name}"
