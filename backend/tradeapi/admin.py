from django.contrib import admin
from .models import TradeBot, TradeBotLog, TradeBotConfig, TradeBotMyAccount, TradeCoinHistory

# Register your models here.
class TradeapiAdmin(admin.ModelAdmin):
    list_display = ('market', 'timestamp', 'trade_price', 'trade_volume', 'ask_bid', 'is_expired', 'is_completed')
    list_filter = ('market', 'timestamp', 'trade_price', 'trade_volume', 'ask_bid', 'is_expired', 'is_completed')
    search_fields = ('market', 'timestamp', 'trade_price', 'trade_volume', 'ask_bid', 'is_expired', 'is_completed')
    ordering = ('market', 'timestamp', 'trade_price', 'trade_volume', 'ask_bid', 'is_expired', 'is_completed')
    readonly_fields = ('timestamp',)

admin.site.register(TradeBot, TradeapiAdmin)