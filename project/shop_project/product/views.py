from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.decorators import api_view,  authentication_classes, permission_classes
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status, authentication, permissions

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from django.db.models import Q

from .models import Comments, Product, Category, Subcategory, Manufacturer
from .serializers import CommentsSerializer, ProductSalesSerializer, ProductSerializer, CategorySerializer, SubcategorySerializer, BrandSerializer, AllCategorySerializer, ProductFilter, ProductDetailSerializer

# инициализация конкретных товаров
class ProductDetail(generics.ListAPIView):
    serializer_class = ProductDetailSerializer
    def get_queryset(self):
        category = self.kwargs['category_slug']
        product = self.kwargs['product_slug']
        queryset =  Product.objects.filter(category__slug = category, slug = product)
        return queryset

# инициализация всех товаров через генерики
class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
        
class CategoryDetail(generics.ListAPIView):
    serializer_class = CategorySerializer

# конкретная категория
class CategoryDetail(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        category = self.kwargs['category_slug']
        queryset = Category.objects.filter(slug=category)
        return self.get_filters(queryset)        

    # фильтрация
    def get_filters(self, queryset):
        # вытаскиваем параметры get запроса в списки
        subcategory_name = self.request.query_params.getlist('sub')
        manufacturer_name = self.request.query_params.getlist('brand')
        # помещаем ограничение по стоимости 
        price = self.request.query_params.get('price')
        price1, price2 = self.validate_get_price(price)
        # помещаем сортировку(order=)
        order_by = self.request.query_params.get('ordering')
        if(order_by == None):
            order_by='pk'


        if subcategory_name or manufacturer_name is not None:
            # помещаем списки параметров в фильтр
            filters = Q()
            # обрабатываем списки и помещаем их содержимое в фильтры
            filters &= self.get_query_params(subcategory_name, "subcategory__name")
            filters &= self.get_query_params(manufacturer_name, "manufacturer__name")
            filters &= Q(price__gte = price1, price__lte = price2)
            # фильтруем
            prefetch_filtered_products = Prefetch(
                'products',
                Product.objects.filter(filters).order_by(order_by)
            )
            return queryset.prefetch_related(prefetch_filtered_products)

        # если никаких фильтров не было
        # или был только price
        prefetch_filtered_products = Prefetch(
            'products', 
            Product.objects.filter(Q(price__gte = price1, price__lte = price2)).order_by(order_by))
        return queryset.prefetch_related(prefetch_filtered_products)


    # преобразуем query параметр в два числа 
    # для последующей фильтрации модели
    def validate_get_price(self, price):
        try:
            price1, price2 = self.get_price(price)
            return price1, price2
        except:
            return 0, 1000000

    def get_price(self, price):
        price = price.split('-')
        return int(price[0]), int(price[1])

    # добавляем список get параметров в Q object 
    def get_query_params(self, query, param):
        filters = Q()
        # параметры добавляются с оператором ИЛИ
        for value in query:
            try:
                filters |= Q(**{param: value})
            except:
                return 0
        return filters
 
# все категории
class AllCategoires(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = AllCategorySerializer

# последние из добавленных товаров
class LastProducts(generics.ListAPIView):
    queryset = Product.objects.all()[:10]
    serializer_class = ProductSerializer
    
class SubcategoryList(generics.ListAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

class BrandList(generics.ListAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = BrandSerializer

class Search(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    # фильтры для поиска
    search_fields = ['name', 'description']
    # поля для сортировки - стоимость, дата создания
    ordering_fields = (
        'price',
        'date_added',
        'sales'
    )

@api_view(['POST'])
def Recommendations(request):
    query = request.data.get('query')
    nonQuery = request.data.get('nonQuery')

    if query and nonQuery:
        # products = Product.objects.filter(category__name=query).exclude(name=nonQuery)
        products = Product.objects.filter(Q(type__icontains=query)).exclude(name=nonQuery)
        serializer = ProductSerializer(products, many=True)
        print(serializer)
        return Response(serializer.data)
    else:
        return Response({"products": []})
    
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def add_comment(request):
    product_id = request.data.pop('product_id')
    comment_serializer = CommentsSerializer(data=request.data)
    if comment_serializer.is_valid():
        comment_serializer.save(user=request.user, product_id = product_id)
        return Response(comment_serializer.data)

class ProductSales(generics.ListAPIView):
    queryset = Product.objects.all().values('name', 'sales').order_by('-sales')
    serializer_class = ProductSalesSerializer

class DeleteComments(generics.DestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer