from django.urls import path

from rest_framework.routers import DefaultRouter

from administration.views import CouponViewSet

router = DefaultRouter()

urlpatterns = [
    path("coupon/<str:code>/", CouponViewSet.as_view({"get": "retrieve"})),
]
urlpatterns += router.urls
