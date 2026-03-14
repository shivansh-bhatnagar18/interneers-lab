from product.models import Product

class ProductRepository:
    def create_product(self, data):
        product = Product(**data)
        product.save()
        return product
    
    def get_all(self):
        return Product.objects()
    
    def get_by_id(self, product_id):
        return Product.objects(id=product_id).first()
    
    def get_by_category(self, category_id):
        return Product.objects(category=category_id)
    
    def update_product(self, product_id, data):
        product = Product.objects(id=product_id).first()
        if product:
            for key, value in data.items():
                setattr(product, key, value)
            product.save()
        return product
    
    def delete_product(self, product_id):
        product = Product.objects(id=product_id).first()
        if product:
            product.delete()
        return product