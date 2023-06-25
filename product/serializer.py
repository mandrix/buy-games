from rest_framework import serializers
from rest_framework.fields import CharField, SerializerMethodField

from product.models import Product, Collectable, VideoGame, Accessory, Console


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

    def create(self, validated_data):
        return super().create(create_product(validated_data))


class ProductSerializer(serializers.ModelSerializer):
    videogame_set = VideoGameSerializer(many=True)
    console_set = ConsoleSerializer(many=True)
    collectable_set = CollectableSerializer(many=True)
    accessory_set = AccessorySerializer(many=True)
    type = SerializerMethodField()

    class Meta:
        model = Product
        fields = ["sale_price", "barcode", "videogame_set", "console_set", "accessory_set", "collectable_set", "type"]

    def get_type(self, obj: Product):
        return obj.get_product_type()
