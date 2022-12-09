from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField("get_quantity")

    class Meta:
        model = Product
        fields = 'id name price quantity'.split()

    def get_quantity(self, obj):
        quantity = self.context.get("cart")[str(obj.id)]["quantity"]
        return quantity


class CartAddSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image_id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = "id title price quantity".split()


# class OrderSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=50)
