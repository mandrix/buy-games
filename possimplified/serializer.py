from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from possimplified.models import Food
from product.models import Product
from product.serializer import TagsSerializer


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"


class ProductPOSSimplifiedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    price = SerializerMethodField()
    name = SerializerMethodField()
    state = serializers.CharField()
    image = SerializerMethodField()
    details = SerializerMethodField()
    tags = TagsSerializer(many=True)

    class Meta:
        model = Product
        fields = ["barcode", "name", "price", "description",
                  "state", "image", "id",
                  "details", "tags"]

    def get_price(self, obj: Product):
        return obj.sale_price

    def get_name(self, obj: Product):
        return str(obj)

    def get_tags(self, obj: Product):
        return [str(tag) for tag in obj.tags.all()]

    def get_image(self, obj: Product):
        request = self.context.get('request', None)
        scheme = 'https://'

        current_site = get_current_site(request) if request else None
        domain = current_site.domain if current_site else ''

        full_url = f'{scheme}{domain}{static("assets/common/default_food.jpg")}'
        if obj.image:
            full_url = obj.image.url
        return full_url

    def get_details(selfself, obj: Product):
        food = obj.food_set.first()
        return FoodSerializer(instance=food).data

