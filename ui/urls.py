from django.urls import path
from ui.views import CountDownView, ReceiptView

urlpatterns = [
    path("receipt",  ReceiptView.as_view()),
    path("",  CountDownView.as_view()),
]
