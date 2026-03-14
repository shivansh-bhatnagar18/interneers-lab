from product_category.models import ProductCategory

class ProductCategoryRepository:

    def create_category(self, title, description=None):
        category = ProductCategory(title=title, description=description)
        category.save()
        return category
    
    def get_category(self, category_id):
        return ProductCategory.objects(id=category_id).first()
    
    def get_all_categories(self):
        return ProductCategory.objects()
    
    def update_category(self, category_id, title=None, description=None):
        category = self.get_category(category_id)
        if not category:
            return None
        if title:
            category.title = title
        if description:
            category.description = description
        category.save()
        return category
    
    def delete_category(self, category_id):
        category = self.get_category(category_id)
        if not category:
            return None
        category.delete()