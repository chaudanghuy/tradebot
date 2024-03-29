from django.urls import path
from . import views

urlpatterns = [
    # home
    path('home', views.TradeBotView.as_view(), name='home'),
    
    # upbit
    path('upbit/account', views.TradeBotAccountView.as_view(), name='upbitAccount'),
    path('upbit/market', views.TradeBotMarketView.as_view(), name='upbitMarket'),
    path('upbit/market/coin', views.TradeBotMarketCoin.as_view(), name='upbitMarketCoin'),
    
    # coin
    path('upbit/coin', views.TradeCoinView.as_view(), name='coin'),
    
    # buy/sale bot
    path('upbit/bot/<str:param>', views.TradeBotCommandView.as_view(), name='upbitBotCommand'),    
    path('upbit/bot/list/<str:param>', views.TradeBotCommandListView.as_view(), name='upbitBotCommandDetail'),    
    
    # bot delete/active/stop
    path('upbit/bot/delete/<str:param>', views.TradeBuyBotCommandDelete.as_view(), name='upbitBotCommandDelete'),
    path('upbit/bot/active/<str:param>', views.TradeBuyBotCommandActive.as_view(), name='upbitBotCommandActive'),
    path('upbit/bot/stop/<str:param>', views.TradeBuyBotCommandStop.as_view(), name='upbitBotCommandStop'),
        
    # log
    path('upbit/bot/log', views.TradeBotCommandLog.as_view(), name='upbitBotLogCommand'),
    
    # setting
    path('upbit/setting', views.TradeBotSettingView.as_view(), name='upbitSetting'),
    path('upbit/setting/update', views.TradeBotSettingUpdate.as_view(), name='upbitSettingDetail'),
    
    # api logout
    path('logout', views.LogoutView.as_view(), name='logout'),    
]
