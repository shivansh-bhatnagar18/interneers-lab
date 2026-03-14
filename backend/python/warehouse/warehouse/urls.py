"""
URL configuration for warehouse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from product.controllers.product_controller import (
    ProductListCreateController,
    ProductDetailController,
    CategoryProductsController,
    ProductCategoryController
)
from product_category.controllers.category_controller import CategoryListCreateController

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', ProductListCreateController.as_view(), name='product-list-create'),
    path('products/<str:product_id>/', ProductDetailController.as_view(), name='product-detail'),
    path('categories/', CategoryListCreateController.as_view(), name='category-list-create'),
    path('categories/<str:category_id>/products/', CategoryProductsController.as_view(), name='category-products'),
    path('products/<str:product_id>/category/', ProductCategoryController.as_view(), name='product-category'),
]
