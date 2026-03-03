from django.db import models
from mongoengine import StringField, FloatField, Document, IntField, DateTimeField
from datetime import datetime

# Create your models here.

class Product(Document):
    name = StringField(required=True, max_length=255)
    description = StringField()
    category = StringField(max_length=255)
    brand = StringField(max_length=255)
    price = FloatField(required=True, min_value=0)
    quantity = IntField(required=True, min_value=0)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'products',
    }