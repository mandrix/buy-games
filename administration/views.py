import datetime

from django.db.models import Value, CharField, F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=False, methods=['post'])
    def list_of_clients(self, request, *args, **kwargs):
        clients = self.queryset.filter(email__icontains=request.data.get("email"))
        clients_serialized = self.serializer_class(
                clients,
                many=True
            )

        return Response(
            clients_serialized.data
        )