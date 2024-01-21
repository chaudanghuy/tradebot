from django.urls import path
from . import views

urlpatterns = [
    # home
    path('home', views.TradeBotView.as_view(), name='home'),
    
    # upbit
    path('upbit/account', views.TradeBotAccountView.as_view(), name='upbit'),
    
    # api logout
    path('logout', views.LogoutView.as_view(), name='logout'),    
]
