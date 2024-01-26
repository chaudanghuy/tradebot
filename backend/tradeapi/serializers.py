from rest_framework import serializers
from .models import TradeBotCommand, TradeBotCommandDetail, TradeBotLog, TradeBotConfig, TradeBotMyAccount, TradeCoinHistory, TradeBotSettingConfig, TradeCoin

class TradeapiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeBotCommand
        fields = '__all__'        
        
class TradeBotCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeBotLog
        fields = '__all__'        

class TradeCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeCoin
        fields = '__all__'           

class TradeBotSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeBotSettingConfig
        fields = '__all__'