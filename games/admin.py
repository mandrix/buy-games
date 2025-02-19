from django.contrib import admin
from product.models import Sale, SaleTypeEnum


class CustomAdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        # Count pending sales
        pending_count = Sale.objects.filter(type=SaleTypeEnum.Pending).count()
        context['pending_payments_count'] = pending_count
        return context

admin_site = CustomAdminSite(name="custom_admin")
