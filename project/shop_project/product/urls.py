from django.urls import path

from product import views

urlpatterns = [
    path('all-categories/', views.AllCategoires.as_view()),
    path('new-products/', views.LastProducts.as_view()),
    path('all-products/', views.ProductList.as_view()),
    path('sub-categories/', views.SubcategoryList.as_view()),
    path('brands/', views.BrandList.as_view()),
    path('sales/', views.ProductSales.as_view()),
    
    path('products/comment/', views.add_comment),
    path('comments/delete/<pk>', views.DeleteComments.as_view()),
    path('products/recommendations/', views.Recommendations),
    path('products/<category_slug>/<product_slug>/', views.ProductDetail.as_view()),
    path('products/<category_slug>/', views.CategoryDetail.as_view()),
    path('products/', views.Search.as_view()),
    path('get_permissions/', views.getUserPermissions),
]