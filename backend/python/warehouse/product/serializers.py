from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False)
    price = serializers.FloatField()
    quantity = serializers.IntegerField()
    brand = serializers.CharField()
    category = serializers.CharField()

    def to_representation(self, instance):
        return {
            "id": str(instance.id),
            "name": instance.name,
            "description": instance.description,
            "category": instance.category,
            "brand": instance.brand,
            "price": instance.price,
            "quantity": instance.quantity,
        }
    