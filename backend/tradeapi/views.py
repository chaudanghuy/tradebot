from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import TradeapiSerializer
from .models import TradeBotCommand, TradeBotCommandDetail, TradeBotLogCommand, TradeBotConfig, TradeBotMyAccount, TradeCoinHistory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from upbit.client import Upbit
import pyupbit
from django.http import JsonResponse
import pandas as pd

# Create your views here.
class TradeapiView(viewsets.ModelViewSet):
    serializer_class = TradeapiSerializer
    queryset = TradeBotCommand.objects.all()
    
class TradeBotView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'JWT Authenticated!'}
        return Response(content)
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class TradeBotAccountView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            access_key = "6j9pBvExB9jWxVwgZb8I6JcsGtOqVSdUUOCNeGBQ"
            screet_key = "2bxUSMoljgnR6c5OhImHUtpJoWH6LY7nF61CdYqH"
            
            # client = Upbit(access_key, screet_key)
            # api_keys = client.APIKey.APIKey_info()
            upbit = pyupbit.Upbit(access_key, screet_key)
            
            return Response(upbit.get_balances())
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)        
        
class TradeBotMarketView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            access_key = "6j9pBvExB9jWxVwgZb8I6JcsGtOqVSdUUOCNeGBQ"
            screet_key = "2bxUSMoljgnR6c5OhImHUtpJoWH6LY7nF61CdYqH"
            
            client = Upbit(access_key, screet_key)
            markets = client.Market.Market_info_all()
                        
            return Response(markets['result'])
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)         

class TradeBotMarketCoin(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            if request.method == 'GET':
                access_key = "6j9pBvExB9jWxVwgZb8I6JcsGtOqVSdUUOCNeGBQ"
                screet_key = "2bxUSMoljgnR6c5OhImHUtpJoWH6LY7nF61CdYqH"
                
                upbit = pyupbit.Upbit(access_key, screet_key)
                
                market = request.GET.get('market')
                
                # current price
                price = pyupbit.get_current_price([{market}])
                
                # get today's candle
                df = pyupbit.get_ohlcv(market, interval="minute1", count=10)                
                
                # candle data            
                formatted_data = []                                
                
                # draw price
                formatted_candle_price = []
                
                for index, row in df.iterrows():
                    formatted_data.append({
                        'timestamp': index.strftime('%Y-%m-%d %H:%M:%S'),
                        'open': row['open'],
                        'close': row['close'],
                        'high': row['high'],
                        'low': row['low'],
                        'volume': row['volume'],
                    })
                    formatted_candle_price.append(row['close'])
                
                formatted_data.sort(key=lambda x: pd.to_datetime(x['timestamp']), reverse=True)
                                
                # draw detecting pump
                
                # get active TradeBotCommand
                # tradeBots = TradeBotCommand.objects.filter(active=True)
                
                # return json response with array has price and formatted_data
                return JsonResponse({
                    'price': price, 
                    'candle': formatted_data,
                    'formatted_candle_price': formatted_candle_price,
                    # 'tradeBots': tradeBots
                }, safe=False)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)   
    
class TradeBotCommandView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            if request.method == 'POST':
                market = request.data['market']
                trade_price = request.data['trade_price']
                trade_volume = request.data['volume']
                ask_bid = request.data['ask_bid']
                
                tradeBotCommand = TradeBotCommand.objects.create(
                    market=market,
                    trade_price=trade_price,
                    trade_volume=trade_volume,
                    ask_bid=ask_bid
                )
                
                return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class TradeBotCommandListView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            if request.method == 'GET':
                bots = TradeBotCommand.objects.all()                
                serializer = TradeapiSerializer(bots, many=True)
                
                return Response(serializer.data)
        except Exception as e:
            return Response(e)        