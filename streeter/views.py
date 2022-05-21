import datetime
import operator
import re

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import filters
from .serializers import StreetSerializer, Street, ShopSerializer, Shop, CitySerializer, City


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CitySerializer
    ordering_fields = ["id"]
    # http_method_names = ["GET", "POST", "PATCH", "DELETE"]


class StreetViewSet(ModelViewSet):
    queryset = Street.objects.all()
    permission_classes = [AllowAny]
    serializer_class = StreetSerializer
    ordering_fields = ["id"]

    def create(self, request: Request, *args, **kwargs):
        street = Street.objects.create(
            name=request.data.get("name"),
            city_id=request.data.get("city")
        )
        data = StreetSerializer(street).data
        return Response(data=data, status=201)


def is_valid_time(time: datetime.time) -> bool:
    pattern = r'([0-1]?[0-9]|2[0-3]):([0-5][0-9])($|:[0-5][0-9])'
    match = re.search(pattern, str(time))
    return True if match else False


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ShopSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id"]

    def list(self, request: Request, *args, **kwargs) -> Response:
        query: dict = request.query_params
        if query and not ((len(query) == 1) and ("ordered_by" in query)):
            ordered_by = query.get("ordered_by")
            shops = Shop.objects.filter(
                city__name__contains=query.get("city", ""),
                street__name__contains=query.get("street", "")
            )
            if ordered_by:
                shops = shops.order_by(ordered_by)
            open_arg = query.get("open")
            if open_arg:
                is_open = int(open_arg)
                current_time = datetime.datetime.now().time()
                new_shop_list = []
                if is_open:
                    for shop in shops:
                        if shop.is_open(current_time):
                            new_shop_list.append(shop)
                else:
                    for shop in shops:
                        if not shop.is_open(current_time):
                            new_shop_list.append(shop)
                data = ShopSerializer(new_shop_list, many=True).data
                return Response(data, status=200)
            data = ShopSerializer(shops, many=True).data
            return Response(data, status=200)
        else:
            return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            if not is_valid_time(request.data.get("open_time")) or not is_valid_time(request.data.get("close_time")):
                raise Exception("Неправильный формат времени")

            street_candidate = Street.objects.get(id=request.data.get("street"))
            if street_candidate.city.id != int(request.data.get("city")):
                raise Exception("Улица не относится к указанному городу")

            shop = Shop.objects.create(
                name=request.data.get("name"),
                house=request.data.get("house"),
                open_time=request.data.get("open_time"),
                close_time=request.data.get("close_time"),
                city_id=request.data.get("city"),
                street_id=request.data.get("street")
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        data = ShopSerializer(shop).data
        return Response(data, status=201)

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        try:
            shop = Shop.objects.get(id=kwargs.get("pk"))
            # @TODO проработать тут обновление города и улицы, а также наборот (улицы и города)
            if "city" in request.data:
                shop.city.id = int(request.data.get("city"))

            if "street" in request.data:
                street_candidate = Street.objects.get(id=request.data.get("street"))
                if street_candidate.city.id != int(shop.city.id):
                    raise Exception("Улица не относится к указанному городу")
                shop.street.id = int(request.data.get("street"))

            if "open_time" in request.data:
                if not is_valid_time(request.data.get("open_time")):
                    raise Exception("Неправильный формат времени (open_time)")
                shop.open_time = request.data.get("open_time")

            if "close_time" in request.data:
                if not is_valid_time(request.data.get("close_time")):
                    raise Exception("Неправильный формат времени (close_time)")
                shop.close_time = request.data.get("close_time")

            if "name" in request.data:
                shop.name = request.data.get("name")
            if "house" in request.data:
                shop.house = request.data.get("house")

            data = ShopSerializer(shop).data
            shop.save()
            return Response(data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class StreetByCityView(APIView):

    def get(self, request: Request, id: int, *args, **kwargs) -> Response:
        city = City.objects.get(id=id)
        streets = city.street_set.all()
        ordered_by = request.query_params.get("ordered_by")
        if ordered_by:
            streets = streets.order_by(ordered_by)
        data = StreetSerializer(streets, many=True).data
        return Response(data, status=200)
