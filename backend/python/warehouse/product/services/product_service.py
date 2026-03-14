from product.repositories.product_repository import ProductRepository
from product_category.models import ProductCategory

class ProductService:

    def __init__(self):
        self.repository = ProductRepository()

    def create_product(self, data):
        category_id = data.get("category")
        category = ProductCategory.objects(id=category_id).first()
        if not category:
            raise ValueError("Invalid category ID.")
        data["category"] = category
        if (data["price"] < 0) or (data["quantity"] < 0):
            raise ValueError("Price and quantity must be non-negative.")
        return self.repository.create_product(data)
    
    def get_products(self):
        return self.repository.get_all()
    
    def get_product(self, product_id):
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found.")
        return product
    
    def update_product(self, product_id, data):
        updated = self.repository.update_product(product_id, data)
        if not updated:
            raise ValueError("Product not found.")
        return updated
    
    def delete_product(self, product_id):
        self.repository.delete_product(product_id)

