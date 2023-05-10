from django.urls import path
from order import views

urlpatterns = [
    path('checkout/', views.checkout),
    path('orders/', views.OrderList.as_view()),
    path('all_orders/', views.AllOrderList.as_view()),
    path('all_orders_list/', views.getAllOrdersByNumber),
    path('change_status/', views.changeOrderStatus),
]