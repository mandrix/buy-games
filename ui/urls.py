from django.urls import path
from ui.views import CountDownView, ReceiptView, GenerateBill, ReturnPolicyView, generate_excel_report

urlpatterns = [
    path("receipt", ReceiptView.as_view()),
    path("", CountDownView.as_view()),
    path("generate-bill", GenerateBill.as_view()),
    path('return-policy/<int:t>/', ReturnPolicyView.as_view(), name='return-policy'),
    path('generate-excel-report/', generate_excel_report, name='generate-excel-report'),
]
