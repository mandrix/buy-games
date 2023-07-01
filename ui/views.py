from django.views.generic import TemplateView


class CountDownView(TemplateView):
    template_name = "coming-soon.html"


class ReceiptView(TemplateView):
    template_name = "receipt.html"
