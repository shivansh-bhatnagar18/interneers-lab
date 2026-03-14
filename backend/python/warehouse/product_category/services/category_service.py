from product_category.repositories.category_repository import ProductCategoryRepository

class ProductCategoryService:
    
    def __init__(self):
        self.repository = ProductCategoryRepository()

    def create_category(self, title, description=None):
        return self.repository.create_category(title, description)

    def get_category(self, category_id):
        category = self.repository.get_category(category_id)
        if not category:
            raise ValueError("Category not found")
        return category
        
    def get_all_categories(self):
        return self.repository.get_all_categories()

    def update_category(self, category_id, title=None, description=None):
        category = self.repository.update_category(category_id, title, description)
        if not category:
            raise ValueError("Category not found")
        return category

    def delete_category(self, category_id):
        category = self.repository.delete_category(category_id)
        if not category:
            raise ValueError("Category not found")
        return category