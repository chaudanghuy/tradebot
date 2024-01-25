from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import TradeapiSerializer, TradeBotCommandSerializer, TradeCoinSerializer
from .models import TradeBotCommand, TradeBotCommandDetail, TradeBotLogCommand1, TradeBotConfig, TradeBotMyAccount, TradeCoinHistory, TradeBuyBotCommand, TradeCoin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from upbit.client import Upbit
import pyupbit
from django.http import JsonResponse
import pandas as pd
import time
from django.conf import settings


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
            access_key = settings.ACCESS_UPBIT_KEY
            screet_key = settings.SECRET_UPBIT_KEY
                        
            upbit = pyupbit.Upbit(access_key, screet_key)
            
            # get list TradeBotCommand with market param and is_completed = 0 and count total                
            tradeBotTotal = TradeBuyBotCommand.objects.filter(is_completed=0).count()
            
            return Response({
                'balances': upbit.get_balances(),
                'total': tradeBotTotal,
            })
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)        
        
class TradeBotMarketView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            access_key = settings.ACCESS_UPBIT_KEY
            screet_key = settings.SECRET_UPBIT_KEY
            
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
                access_key = settings.ACCESS_UPBIT_KEY
                screet_key = settings.SECRET_UPBIT_KEY
                
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
                is_detecting_pump = False;
                df = pyupbit.get_ohlcv(market, "minute1", 20)
                try:
                    data_count = 20
                    add_average_min_df = df['volume'].rolling(window=10).mean().shift(1)
                    average_vol = add_average_min_df['average'][data_count-1]
                    now_vol = add_average_min_df['volume'][data_count-1]                                        
                        
                    # Up or Down
                    last_close = add_average_min_df['close'][-1]
                    last_open_price = add_average_min_df['open'][-1]                    
                    status = 20
                    if last_close - last_open_price > 0:
                        status = 10
                            
                    if status == 10:
                        compare_vol = average_vol*7
                        if now_vol >= compare_vol:     
                            is_detecting_pump = True
                except:
                    is_detecting_pump = False                                                    
                
                # tradeBots = TradeBotCommand.objects.filter(active=True)
                
                # return json response with array has price and formatted_data
                return JsonResponse({
                    'price': price, 
                    'candle': formatted_data,
                    'formatted_candle_price': formatted_candle_price,                    
                    'is_detecting_pump': is_detecting_pump,                    
                }, safe=False)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)   
    
class TradeBotCommandView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, param):
        try:
            if request.method == 'POST':                                    
                market = request.data['market']
                trade_price = request.data['trade_price']
                trade_volume = request.data['volume']
                ask_bid = request.data['ask_bid']
                
                if (param == 'buy'):
                    tradeBotCommand = TradeBuyBotCommand.objects.create(
                        market=market,
                        trade_price=trade_price,
                        trade_volume=trade_volume,
                        ask_bid=ask_bid
                    )
                else:
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
    def get(self, request, param):
        
        access_key = settings.ACCESS_UPBIT_KEY
        screet_key = settings.SECRET_UPBIT_KEY                
        upbit = pyupbit.Upbit(access_key, screet_key)     
        
        balance = upbit.get_balance("KRW")  

        try:
            if request.method == 'GET':
                # get list bots with is_completed = 0         
                if (param == 'buy'):
                    bots = TradeBuyBotCommand.objects.filter(is_completed=0)                                                          
                else:
                    bots = TradeBotCommand.objects.filter(is_completed=0)                                  
                serializer = TradeapiSerializer(bots, many=True)                                                                        
                return Response(serializer.data)                       
        except Exception as e:
            if (param == 'buy'):
                bots = TradeBuyBotCommand.objects.filter(is_completed=0)                                                          
            else:
                bots = TradeBotCommand.objects.filter(is_completed=0)
            serializer = TradeapiSerializer(bots, many=True)                                                                        
            return Response(serializer.data)

class TradeBotCommandDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, param):
        try:
            # find bot by market param
            bot = TradeBotCommand.objects.filter(market=param).update(is_completed=1)            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class TradeBuyBotCommandDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, param):
        try:
            # find bot by market param and delete            
            bot = TradeBuyBotCommand.objects.filter(market=param).delete()                        
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)        
        
class TradeBuyBotCommandActive(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, param):
        try:
            # find bot by market param and change to is_completed           
            bot = TradeBuyBotCommand.objects.filter(market=param).update(is_expired=0)                        
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        
class TradeBuyBotCommandStop(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, param):
        try:
            # find bot by market param and change to is_completed           
            bot = TradeBuyBotCommand.objects.filter(market=param).update(is_expired=1)                        
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)           
        
class TradeBotCommandLog(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:                                    
            logs = TradeBotLogCommand1.objects.filter(is_error=False).order_by('-timestamp')[:10]
            serializer = TradeBotCommandSerializer(logs, many=True)                                                                        
            return Response(serializer.data)                       
        except Exception as e:
            return Response(e)                    
        
class TradeCoinView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            coins = TradeCoin.objects.all()            
            serializer = TradeCoinSerializer(coins, many=True)                                                                        
            return Response(serializer.data)                       
        except Exception as e:
            return Response(e)        
