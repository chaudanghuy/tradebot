from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TradeapiSerializer
from .models import TradeBot, TradeBotLog, TradeBotConfig, TradeBotMyAccount, TradeCoinHistory

# Create your views here.
class TradeapiView(viewsets.ModelViewSet):
    serializer_class = TradeapiSerializer
    queryset = TradeBot.objects.all()