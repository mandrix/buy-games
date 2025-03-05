from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from product.models import Sale, SaleTypeEnum


class CustomAdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        # Count pending sales
        pending_count = Sale.objects.filter(type=SaleTypeEnum.Pending).count()
        context['pending_payments_count'] = pending_count
        return context

    def get_app_list(self, request, app_label=None):
        """ Filter app list to show User and Group models only if the user is in 'All Access'. """
        app_list = super().get_app_list(request, app_label)
        if not request.user.groups.filter(name="All Access").exists():
            # Remove User and Group models from the displayed list
            for app in app_list:
                app["models"] = [
                    model for model in app["models"]
                    if model["object_name"] not in ["User", "Group", "Food", "Logs"]
                ]
        if request.user.groups.filter(name="Restaurant").exists():
            # Remove User and Group models from the displayed list
            for app in app_list:
                app["models"] = [
                    model for model in app["models"]
                    if model["object_name"] not in [
                                                        "Location", "Requests", "Settings", "Payments"
                                                    ]
                ]
        return app_list

admin_site = CustomAdminSite(name="custom_admin")

admin_site.register(User, UserAdmin)
admin_site.register(Group)


