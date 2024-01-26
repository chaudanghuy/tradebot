from django.contrib import admin
from .models import TradeBuyBotCommand, TradeCoin, TradeBotLog, TradeBotSettingConfig

# Register your models here.
class TradeBuyBotCommandAdmin(admin.ModelAdmin):
    list_display = ('market', 'timestamp', 'trade_volume', 'ask_bid', 'is_expired', 'is_completed')    
    
admin.site.register(TradeBuyBotCommand, TradeBuyBotCommandAdmin)    

class TradeCoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'market')    

admin.site.register(TradeCoin, TradeCoinAdmin)

class TradeBotLogAdmin(admin.ModelAdmin):
    list_display = ('message', 'trade_market', 'timestamp')
    
admin.site.register(TradeBotLog, TradeBotLogAdmin)    

class TradeBotSettingAdmin(admin.ModelAdmin):
    list_display = ('accessKey', 'secretKey', 'currency', 'time_sleep', 'timestamp', 'pumping_rate', 'is_active')

admin.site.register(TradeBotSettingConfig, TradeBotSettingAdmin)    