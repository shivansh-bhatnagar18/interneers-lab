from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class ProductCategory(Document):
    title = StringField(required=True, unique=True, max_length=255)
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'product_categories',
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(ProductCategory, self).save(*args, **kwargs)