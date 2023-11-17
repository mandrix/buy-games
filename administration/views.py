import datetime

from rest_framework import viewsets

from administration.models import Coupon
from administration.serializer import CouponSerializer


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.filter(expiration__gt=datetime.datetime.now())
    serializer_class = CouponSerializer
    permission_classes = []
    lookup_field = "code"
