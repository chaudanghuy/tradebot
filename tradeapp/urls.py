from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),     
     path('get_order_book', views.get_order_book, name='get_order_book'),
     path('get_coin_price', views.get_coin_price, name='get_coin_price'),
     path('create_order', views.create_order, name='create_order'),
     path('order_list', views.order_list, name='order_list'),
]
