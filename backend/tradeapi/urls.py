from django.urls import path
from . import views

urlpatterns = [
    # home
    path('home', views.TradeBotView.as_view(), name='home'),
    
    # upbit
    path('upbit/account', views.TradeBotAccountView.as_view(), name='upbitAccount'),
    path('upbit/market', views.TradeBotMarketView.as_view(), name='upbitMarket'),
    path('upbit/market/coin', views.TradeBotMarketCoin.as_view(), name='upbitMarketCoin'),
    path('upbit/bot', views.TradeBotCommandView.as_view(), name='upbitBotCommand'),
    path('upbit/bot/list', views.TradeBotCommandListView.as_view(), name='upbitBotCommandDetail'),
    path('upbit/bot/delete/<str:param>', views.TradeBotCommandDelete.as_view(), name='upbitBotCommandDelete'),
    path('upbit/bot/log', views.TradeBotCommandLog.as_view(), name='upbitBotLogCommand'),
    
    # api logout
    path('logout', views.LogoutView.as_view(), name='logout'),    
]
