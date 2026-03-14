from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.serializers import ProductSerializer
from product.services.product_service import ProductService

class CategoryProductsController(APIView):
    def __init__(self):
        self.service = ProductService()

    def get(self, request, category_id):
        try:
            products = self.service.get_products_by_category(category_id)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
class ProductCategoryController(APIView):

    def __init__(self):
        self.service = ProductService()

    def delete(self, request, product_id):
        try:
            product = self.service.remove_category(product_id)
            return Response(ProductSerializer(product).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, product_id):
        category_id = request.data.get("category")
        if not category_id:
            return Response({"error": "Category ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = self.service.assign_category(product_id, category_id)
            return Response(ProductSerializer(product).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductListCreateController(APIView):
    def __init__(self):
        self.service = ProductService()

    def get(self, request):
        product = self.service.get_products()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = self.service.create_product(serializer.validated_data)
                return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetailController(APIView):
    def __init__(self):
        self.service = ProductService()

    def get(self, request, product_id):
        try:
            product = self.service.get_product(product_id)
            return Response(ProductSerializer(product).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, product_id):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                updated_product = self.service.update_product(product_id, serializer.validated_data)
                return Response(ProductSerializer(updated_product).data)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        try:
            self.service.delete_product(product_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)