from django.contrib import admin
from .models import TradeBotCommand, TradeBotCommandDetail, TradeBotLogCommand1, TradeBotConfig, TradeBotMyAccount, TradeCoinHistory

# Register your models here.
class TradeapiAdmin(admin.ModelAdmin):
    list_display = ('market', 'timestamp', 'trade_price', 'trade_volume', 'ask_bid', 'is_expired', 'is_completed')
    list_filter = ('market', 'timestamp', 'trade_price', 'trade_volume', 'ask_bid', 'is_expired', 'is_completed')
    search_fields = ('market', 'timestamp', 'trade_price', 'trade_volume', 'ask_bid', 'is_expired', 'is_completed')
    ordering = ('market', 'timestamp', 'trade_price', 'trade_volume', 'ask_bid', 'is_expired', 'is_completed')
    readonly_fields = ('timestamp',)

admin.site.register(TradeBotCommand, TradeapiAdmin)

class TradeBotLogCommandAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'message', 'is_error', 'trade_market')
    list_filter = ('timestamp', 'message', 'is_error', 'trade_market')
    search_fields = ('timestamp', 'message', 'is_error', 'trade_market')
    ordering = ('timestamp', 'message', 'is_error', 'trade_market')
    readonly_fields = ('timestamp',)

admin.site.register(TradeBotLogCommand1, TradeBotLogCommandAdmin)    