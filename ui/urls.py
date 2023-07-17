from django.urls import path
from ui.views import CountDownView, ReceiptView, GenerateBill, ReturnPolicyView

urlpatterns = [
    path("receipt", ReceiptView.as_view()),
    path("", CountDownView.as_view()),
    path("generate-bill", GenerateBill.as_view()),
    path('return-policy/', ReturnPolicyView.as_view(), name='return-policy'),
]
