from django.contrib import admin
from .models import TradeBuyBotCommand, TradeCoin, TradeBotLogCommand1

# Register your models here.
class TradeBuyBotCommandAdmin(admin.ModelAdmin):
    list_display = ('market', 'timestamp', 'trade_price', 'trade_volume', 'ask_bid', 'is_expired', 'is_completed')    
    
admin.site.register(TradeBuyBotCommand, TradeBuyBotCommandAdmin)    

class TradeCoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'market')    

admin.site.register(TradeCoin, TradeCoinAdmin)

class TradeBotLogCommandAdmin(admin.ModelAdmin):
    list_display = ('message', 'trade_market', 'timestamp')
    
admin.site.register(TradeBotLogCommand1, TradeBotLogCommandAdmin)    