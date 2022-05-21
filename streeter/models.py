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

    def compare_date(self) -> bool:
        """
        Возвращает True, если время открытия меньше времени закрытия (10:00-22:00) и
        возвращает False, если время открытия больше времени закрытия (22:00-10:00)
        :return: bool
        """
        if self.open_time > self.close_time:
            return False
        else:
            return True

    def is_open(self, current_time: time) -> bool:
        # 22:00-02:00, 21:24
        # 22:00 <= 21:24 True                   <--|-\
        # <========================================|===========<|>
        # 02:00+24:00=26:00 >= 21:24 True       <--|-/
        if self.open_time > self.close_time:
            th, tm, ts = self.close_time.hour, self.close_time.minute, self.close_time.second
            new_close_time = datetime(year=1, month=1, day=2, hour=th, minute=tm, second=ts)
            new_current_time = datetime(year=1, month=1, day=1, hour=current_time.hour, minute=current_time.minute, second=current_time.second)
            if (self.open_time <= current_time) and (new_close_time >= new_current_time):
                return True
            else:
                return False
        else:
            if (self.open_time <= current_time) and (self.close_time >= current_time):
                return True
            else:
                return False

    def __str__(self):
        return f"{self.id}. {self.city.name} -> {self.name}"
