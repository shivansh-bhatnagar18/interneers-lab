from product.repositories.product_repository import ProductRepository

class ProductService:

    def __init__(self):
        self.repository = ProductRepository()

    def create_product(self, data):
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

