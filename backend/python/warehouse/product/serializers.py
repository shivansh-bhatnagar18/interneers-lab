from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False)
    price = serializers.FloatField()
    quantity = serializers.IntegerField()
    brand = serializers.CharField(required=True)
    category = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def to_representation(self, instance):
        return {
            "id": str(instance.id),
            "name": instance.name,
            "description": instance.description,
            "category": {
                "id": str(instance.category.id),
                "title": instance.category.title
            },
            "brand": instance.brand,
            "price": instance.price,
            "quantity": instance.quantity,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }
    