import datetime
import re

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import filters
from django.db.models import F, Expression, Q
from .serializers import StreetSerializer, Street, ShopSerializer, Shop, CitySerializer, City, ShopReturnSerializer


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CitySerializer
    ordering_fields = ["id"]
    http_method_names = ["get", "post", "patch", "delete"]


class StreetViewSet(ModelViewSet):
    queryset = Street.objects.all()
    permission_classes = [AllowAny]
    serializer_class = StreetSerializer
    ordering_fields = ["id"]
    http_method_names = ["get", "post", "patch", "delete"]

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
    http_method_names = ["get", "post", "patch", "delete"]

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
                is_open = bool(int(open_arg))
                current_date = datetime.datetime.now().time()
                shops = shops.filter(open_time__lt=current_date, close_time__gt=current_date)
                # if ...:
                #     shops = shops.extra(where=["localtime between open_time and close_time"])
                # else:
                #     shops = shops.extra(where=["localtime not between open_time and close_time"])
                # shops = [shop for shop in shops if shop.is_open is is_open]
            data = ShopSerializer(shops, many=True).data
            return Response(data, status=200)
        else:
            return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs) -> Response:
        try:
            open_time = datetime.datetime.strptime(request.data.get("open_time"), "%H:%M")
            close_time = datetime.datetime.strptime(request.data.get("close_time"), "%H:%M")
            if open_time > close_time:
                close_time += datetime.timedelta(days=1)
            # request.data["open_time"] = new_open_time
            request.data["open_time"] = open_time
            request.data["close_time"] = close_time
            serializer = super().get_serializer_class()
            serializer_instance: ShopSerializer = serializer(data=request.data)
            serializer_instance.is_valid(raise_exception=True)
            shop = serializer_instance.save(**serializer_instance.validated_data)
            return Response(ShopReturnSerializer(shop).data, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        try:
            obj = self.get_object()
            serializer = ShopSerializer(obj, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_shop = serializer.update(obj, serializer.validated_data)
            return Response(ShopReturnSerializer(updated_shop).data, status=200)
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
