from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product_category.services.category_service import ProductCategoryService
from product_category.serializers import ProductCategorySerializer

class CategoryListCreateController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductCategoryService()

    def get(self, request):
        categories = self.service.get_all_categories()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = self.service.create_category(
                title=serializer.validated_data['title'],
                description=serializer.validated_data.get('description', '')
            )
            return Response(ProductCategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)