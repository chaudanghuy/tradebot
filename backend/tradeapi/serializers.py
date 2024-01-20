from rest_framework import serializers
from .models import TradeBot, TradeBotLog, TradeBotConfig, TradeBotMyAccount, TradeCoinHistory

class TradeapiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeBot
        fields = '__all__'