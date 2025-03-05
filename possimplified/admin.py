from django.contrib import admin

from games.admin import admin_site
from possimplified.models import Food


class FoodAdmin(admin.ModelAdmin):
    model = Food


admin_site.register(Food, FoodAdmin)
