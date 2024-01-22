from rest_framework import serializers
from rest_framework.fields import CharField, SerializerMethodField

from product.models import Product, Collectable, VideoGame, Accessory, Console, Report, Sale, Payment


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


class ProductSerializer(serializers.ModelSerializer):
    price = SerializerMethodField()
    name = SerializerMethodField()
    videogame_set = VideoGameSerializer(many=True)
    console_set = ConsoleSerializer(many=True)
    collectable_set = CollectableSerializer(many=True)
    accessory_set = AccessorySerializer(many=True)
    type = SerializerMethodField()
    payment = PaymentSerializer(required=True)

    class Meta:
        model = Product
        fields = ["payment", "barcode", "name", "price", "description",
                  "videogame_set", "console_set", "accessory_set", "collectable_set", "type"]

    def get_type(self, obj: Product):
        try:
            return obj.get_product_type()
        except:
            return "N/A"

    def get_price(self, obj: Product):
        return obj.sale_price

    def get_name(self, obj: Product):
        return str(obj)


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
