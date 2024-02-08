from django.urls import path

from rest_framework.routers import DefaultRouter

from administration.views import CouponViewSet, ClientViewSet

router = DefaultRouter()

urlpatterns = [
    path("coupon/<str:code>/", CouponViewSet.as_view({"get": "retrieve"})),
    path("client/<str:email>/", ClientViewSet.as_view({"get": "retrieve"})),
    path("clients/", ClientViewSet.as_view({"post": "list_of_clients"})),
]
urlpatterns += router.urls
