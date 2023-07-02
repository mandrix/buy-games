from django.urls import path
from ui.views import CountDownView, ReceiptView, GenerateBill


urlpatterns = [
    path("receipt",  ReceiptView.as_view()),
    path("",  CountDownView.as_view()),
    path("generate-bill",  GenerateBill.as_view()),
]
