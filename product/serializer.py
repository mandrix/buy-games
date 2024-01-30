from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from rest_framework import serializers
from rest_framework.fields import CharField, SerializerMethodField, URLField

from product.models import Product, Collectable, VideoGame, Accessory, Console, Report, Sale, Payment, Tag


def create_product(validated_data):
    nested_data = validated_data['product']
    if nested_data is not None:
        validated_data["product"] = Product.objects.create(**nested_data)
    return validated_data


class CollectableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collectable
        fields = "__all__"

    def create(self, validated_data):
        return super().create(create_product(validated_data))


class VideoGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGame
        fields = "__all__"

    def create(self, validated_data):
        return super().create(create_product(validated_data))


class AccessorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessory
        fields = "__all__"

    def create(self, validated_data):
        return super().create(create_product(validated_data))


class ConsoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Console
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['title'] = instance.get_title_display()
        return representation

    def create(self, validated_data):
        return super().create(create_product(validated_data))


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def to_representation(self, instance):
        payment_info = instance.check_payment()
        return payment_info


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class FullURLField(serializers.URLField):
    def to_representation(self, value):
        request = self.context.get('request', None)
        scheme = 'https://'

        current_site = get_current_site(request) if request else None
        domain = current_site.domain if current_site else ''


        full_url = f'{scheme}{domain}/media/{value}'
        if not value:
            full_url = f'{scheme}{domain}{static("default.jpg")}'
        return super().to_representation(full_url)

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    price = SerializerMethodField()
    name = SerializerMethodField()
    videogame_set = VideoGameSerializer(many=True)
    console_set = ConsoleSerializer(many=True)
    collectable_set = CollectableSerializer(many=True)
    accessory_set = AccessorySerializer(many=True)
    type = SerializerMethodField()
    payment = PaymentSerializer(required=True)
    image = SerializerMethodField()
    console = SerializerMethodField()
    tags = TagsSerializer(many=True)

    class Meta:
        model = Product
        fields = ["payment", "barcode", "name", "price", "description", "videogame_set",
                  "console_set", "accessory_set", "collectable_set", "type", "image", "id",
                  "console", "tags", "used"]

    def get_type(self, obj: Product):
        try:
            return obj.get_product_type()
        except:
            return "N/A"

    def get_price(self, obj: Product):
        return obj.sale_price

    def get_name(self, obj: Product):
        return str(obj)

    def get_console(self, obj: Product):
        if type(obj.get_additional_product_info()) == Collectable:
            console_code = ""
        else:
            console_code = obj.get_additional_product_info().title if type(obj.get_additional_product_info()) == Console else obj.get_additional_product_info().console
        return {"console": str(obj.console_type), "console-code": console_code}

    def get_tags(self, obj: Product):
        return [str(tag) for tag in obj.tags.all()]

    def get_image(self, obj: Product):
        request = self.context.get('request', None)
        scheme = 'https://'

        current_site = get_current_site(request) if request else None
        domain = current_site.domain if current_site else ''


        full_url = f'{scheme}{domain}{static("default.jpg")}'
        if obj.image:
            full_url = obj.image.url
        return full_url



class ProductSerializerToShow(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    products = ProductSerializerToShow(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    sales = SaleSerializer(many=True, read_only=True, source='sale_set')

    class Meta:
        model = Report
        fields = '__all__'
