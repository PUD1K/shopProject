from cgitb import lookup
from rest_framework import serializers
from django_filters import FilterSet
from django_filters import NumberFilter, AllValuesFilter,  MultipleChoiceFilter, AllValuesMultipleFilter

from .models import Category, Manufacturer, Product, Subcategory

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    subcategory = serializers.SlugRelatedField(slug_field="name", read_only=True)
    manufacturer = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Product
        fields=(
            'id',
            'name',
            'category', 
            'subcategory',
            'manufacturer',
            'get_absolute_url',
            'description',
            'price',
            'get_image',
            'get_thumbnail',

            'type',
            'processor',
            'videocart',
            'hdd',
            'ram'
        )  

class ProductFilter(FilterSet):
    # интферфейс взаимодействия полей фильтров
    # price на основе orm gte и lte(больше меньше)
    min_price = NumberFilter(field_name = 'price', lookup_expr = 'gte' )
    max_price = NumberFilter(field_name = 'price', lookup_expr = 'lte')
    # для поиска аналогично - %ILIKE%
    category_name = AllValuesMultipleFilter(field_name = 'category__name')
    subcategory_name = AllValuesMultipleFilter(field_name = 'subcategory__name')
    manufacturer_name = AllValuesMultipleFilter(field_name = 'manufacturer__name')

    # инициализация полей фильтров
    class Meta:
        model = Product
        fields = (
            'name',
            'min_price',
            'max_price',
            'category_name',
            'subcategory_name',
            'manufacturer_name',
        )

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields=(
            'id',
            'name',
            'get_absolute_url',
            'products'
        )

class AllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=(
            'id',
            'name',
            'get_absolute_url',
        )
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields=(
            'name',
            'slug'
        )

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields=(
            'name',
            'slug'
        )
