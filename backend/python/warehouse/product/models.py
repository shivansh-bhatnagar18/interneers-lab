from django.db import models
from mongoengine import StringField, FloatField, Document, IntField, DateTimeField, ReferenceField
from datetime import datetime
from product_category.models import ProductCategory

# Create your models here.

class Product(Document):
    name = StringField(required=True, max_length=255)
    description = StringField()
    category = ReferenceField(ProductCategory, required=True)
    brand = StringField(max_length=255)
    price = FloatField(required=True, min_value=0)
    quantity = IntField(required=True, min_value=0)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'products',
    }