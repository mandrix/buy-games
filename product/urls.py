from django.urls import path

from rest_framework.routers import DefaultRouter

from product.views import ProductViewSet, CollectableViewSet, VideoGameViewSet, AccessoryViewSet, ReportViewSet, \
    DailySalesReport

router = DefaultRouter()
router.register(r'reports', ReportViewSet)

urlpatterns = [
    path("products/", ProductViewSet.as_view({"post": "create", "get": "list"})),
    path("product/<str:pk>/", ProductViewSet.as_view({"get": "retrieve"})),
    path("collectable/", CollectableViewSet.as_view({"post": "create", "get": "list"})),
    path("video-game/", VideoGameViewSet.as_view({"post": "create", "get": "list"})),
    path("accessory/", AccessoryViewSet.as_view({"post": "create", "get": "list"})),
    path('sales/', DailySalesReport.as_view(), name='daily-sales-report'),
]
urlpatterns += router.urls
