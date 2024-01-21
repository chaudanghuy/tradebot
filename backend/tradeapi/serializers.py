from rest_framework import serializers
from .models import TradeBotCommand, TradeBotCommandDetail, TradeBotLogCommand, TradeBotConfig, TradeBotMyAccount, TradeCoinHistory, TradeBotSetting

class TradeapiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeBotCommand
        fields = '__all__'        