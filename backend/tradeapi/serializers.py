from rest_framework import serializers
from .models import TradeBotCommand, TradeBotCommandDetail, TradeBotLogCommand1, TradeBotConfig, TradeBotMyAccount, TradeCoinHistory, TradeBotSetting

class TradeapiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeBotCommand
        fields = '__all__'        
        
class TradeBotCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeBotLogCommand1
        fields = '__all__'        