import datetime

from django.db.models import Value, CharField, F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from administration.models import Coupon, Client
from administration.serializer import CouponSerializer, ClientSerializer
from product.views import Throttling

import requests
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings

class CouponViewSet(viewsets.ModelViewSet, Throttling):
    queryset = Coupon.objects.filter(expiration__gt=datetime.datetime.now())
    serializer_class = CouponSerializer
    permission_classes = []
    lookup_field = "code"


class ClientViewSet(viewsets.ModelViewSet, Throttling):
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
        
class CreateCustomer(APIView):
    def post(self, request, *args, **kwargs):
        payload = {
            "name": request.data.get("name"),
            "email": request.data.get("email"),
            "description": request.data.get("description")
        }
        headers = {"Authorization": f"Bearer {settings.ONVOPAY_API_KEY}"}

        try:
            response = requests.post('https://api.onvopay.com/v1/customers', json=payload, headers=headers)
            response.raise_for_status()
            return Response({"customerData": response.json()}, status=status.HTTP_200_OK)
        except requests.exceptions.HTTPError as err:
            return Response({"error": str(err)}, status=err.response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CreatePaymentMethod(APIView):
    def post(self, request, *args, **kwargs):
        payload = {
            "type": "card",
            "card": {
                "number": request.data.get("number"),
                "expMonth": request.data.get("expMonth"),
                "expYear": request.data.get("expYear"),
                "cvv": request.data.get("cvv"),
                "holderName": request.data.get("holderName")
            }
            # "customerId": request.data.get("customerId")
        }
        headers = {"Authorization": f"Bearer {settings.ONVOPAY_API_KEY}"}

        try:
            response = requests.post('https://api.onvopay.com/v1/payment-methods', json=payload, headers=headers)
            response.raise_for_status()
            return Response({"paymentMethod": response.json()}, status=status.HTTP_200_OK)
        except requests.exceptions.HTTPError as err:
            print(err)
            return Response({"error": str(err)}, status=err.response.status_code)
        except requests.exceptions.RequestException as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CreatePaymentIntent(APIView):
    def post(self, request, *args, **kwargs):
        payload = {
            "amount": request.data.get("amount"),
            "currency": request.data.get("currency"),
            # "customerId": request.data.get("customerId"),
            "description": request.data.get("description"),
            "metadata":{
                "userId":request.data.get("userId"),
                "phoneNumber":request.data.get("phoneNumber"),
                "userName":request.data.get("userName"),
                "userEmail":request.data.get("userEmail")
            }
        }
        headers = {"Authorization": f"Bearer {settings.ONVOPAY_API_KEY}"}

        try:
            response = requests.post('https://api.onvopay.com/v1/payment-intents', json=payload, headers=headers)
            response.raise_for_status()
            return Response({"paymentIntent": response.json()}, status=status.HTTP_200_OK)
        except requests.exceptions.HTTPError as err:
            print(err)
            return Response({"error": str(err)}, status=err.response.status_code)
        except requests.exceptions.RequestException as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ConfirmPaymentIntent(APIView):
    def post(self, request, *args, **kwargs):
        paymentIntentId = request.data.get("paymentIntentId")
        paymentMethodId = request.data.get("paymentMethodId")

        if not paymentIntentId or not paymentMethodId:
            return Response({"error": "Payment Intent ID and Payment Method ID are required"}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            "Authorization": f"Bearer {settings.ONVOPAY_API_KEY}"
        }

        try:
            response = requests.post(
                f'https://api.onvopay.com/v1/payment-intents/{paymentIntentId}/confirm',
                json={"paymentMethodId": paymentMethodId},
                headers=headers
            )
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.HTTPError as err:
            print(err)
            return Response({"error": str(err)}, status=err.response.status_code)
        except requests.exceptions.RequestException as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)