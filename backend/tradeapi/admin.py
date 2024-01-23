from django.contrib import admin
from .models import TradeBuyBotCommand, TradeCoin

# Register your models here.
class TradeBuyBotCommandAdmin(admin.ModelAdmin):
    list_display = ('market', 'timestamp', 'trade_price', 'trade_volume', 'ask_bid', 'is_expired', 'is_completed')    
    
admin.site.register(TradeBuyBotCommand, TradeBuyBotCommandAdmin)    

class TradeCoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'market')    

admin.site.register(TradeCoin, TradeCoinAdmin)