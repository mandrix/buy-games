import datetime

from rest_framework import viewsets

from administration.models import Coupon, Client
from administration.serializer import CouponSerializer, ClientSerializer


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.filter(expiration__gt=datetime.datetime.now())
    serializer_class = CouponSerializer
    permission_classes = []
    lookup_field = "code"


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = []
    lookup_field = "email"