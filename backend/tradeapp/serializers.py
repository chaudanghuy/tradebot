from rest_framework import serializers
from .models import Order, BotCoin

class TradeAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class BotCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotCoin
        fields = '__all__'