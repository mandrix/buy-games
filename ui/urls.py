from django.urls import path
from ui.views import CountDownView, ReceiptView, GenerateBill, ReturnPolicyView, generate_excel_report, ReportView, \
    CalculateTotalView, CalculatePayNewProduct

urlpatterns = [
    path("receipt", ReceiptView.as_view()),
    path("report", ReportView.as_view()),
    path("", CountDownView.as_view()),
    path("generate-bill", GenerateBill.as_view()),
    path('return-policy/<int:t>/', ReturnPolicyView.as_view(), name='return-policy'),
    path('generate-excel-report/<str:fecha>/', generate_excel_report, name='generate-excel-report'),
    path('calculate-total/', CalculateTotalView.as_view(), name='calculate-total'),
    path('calculate-price-order/', CalculatePayNewProduct.as_view(), name='calculate-price-order'),

]
