from rest_framework import serializers

from product.models import Product, Collectable, VideoGame, Accessory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


def create_product(validated_data):
    nested_data = validated_data['product']
    if nested_data is not None:
        validated_data["product"] = Product.objects.create(**nested_data)
    return validated_data


class CollectableSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Collectable
        fields = "__all__"

    def create(self, validated_data):
        return super().create(create_product(validated_data))


class VideoGameSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = VideoGame
        fields = "__all__"

    def create(self, validated_data):
        return super().create(create_product(validated_data))


class AccessorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Accessory
        fields = "__all__"

    def create(self, validated_data):
        return super().create(create_product(validated_data))
