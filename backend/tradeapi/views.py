from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import TradeapiSerializer, TradeBotCommandSerializer
from .models import TradeBotCommand, TradeBotCommandDetail, TradeBotLogCommand1, TradeBotConfig, TradeBotMyAccount, TradeCoinHistory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from upbit.client import Upbit
import pyupbit
from django.http import JsonResponse
import pandas as pd
import time


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
                
                
                # get list TradeBotCommand with market param and is_completed = 0 and count total                
                tradeBotTotal = TradeBotCommand.objects.filter(market=market, is_completed=0).count()
                
                # tradeBots = TradeBotCommand.objects.filter(active=True)
                
                # return json response with array has price and formatted_data
                return JsonResponse({
                    'price': price, 
                    'candle': formatted_data,
                    'formatted_candle_price': formatted_candle_price,
                    'tradeBotTotal': tradeBotTotal,
                    'is_detecting_pump': is_detecting_pump,
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
                # get list bots with is_completed = 0                
                bots = TradeBotCommand.objects.filter(is_completed=0)            
                
                # loop through bots and check if it is up or down
                market_list_monitor = []
                for bot in bots:                    
                    ticker = bot.market
                    data_count = 20
                    df = pyupbit.get_ohlcv(ticker, "minute1", 20)
                    try:
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
                                bot.is_completed = 1
                                bot.save()            
                                botLog = TradeBotLogCommand1.objects.create(
                                    message="detecting pump and create command to buy " + ticker,
                                    is_error=False,
                                    trade_market=ticker
                                );           
                                print('\033[30m', time.strftime('%m-%d %H:%M:%S'), ticker, "구매")                        
                                # buy_log = upbit.buy_market_order(ticker, total_weight)                                                       
                    except:                        
                        bot.is_completed = 0
                        bot.save()                                                
                        # log
                        TradeBotLogCommand1.objects.create(
                            message="no detecting pump for " + ticker,
                            is_error=True,
                            trade_market=ticker
                        );                                                                                                                                                                                                                               
                                
                # get fresh list bots
                bots = TradeBotCommand.objects.filter(is_completed=0)                                
                serializer = TradeapiSerializer(bots, many=True)                                                                        
                return Response(serializer.data)                       
        except Exception as e:
            return Response(e)        
        
    def is_up_or_down(self, df):
        last_close = df['close'][-1]
        last_open_price = df['open'][-1]
        if last_close - last_open_price > 0:
            return self.GRAPH_UP
        else:
            return self.GRAPH_DOWN
        
    def make_df_add_average_volume(ticker, interval, rolling_value, count=20):
        try:
            access_key = "6j9pBvExB9jWxVwgZb8I6JcsGtOqVSdUUOCNeGBQ"
            screet_key = "2bxUSMoljgnR6c5OhImHUtpJoWH6LY7nF61CdYqH"
                
            upbit = pyupbit.Upbit(access_key, screet_key)
            df = pyupbit.get_ohlcv(ticker, interval, count)

            df['average'] = df['volume'].rolling(window=rolling_value).mean().shift(1)            
            return df
        except:
            return 1
    
    def buy_process(self, ticker, total_weight):
        try:
            access_key = "6j9pBvExB9jWxVwgZb8I6JcsGtOqVSdUUOCNeGBQ"
            screet_key = "2bxUSMoljgnR6c5OhImHUtpJoWH6LY7nF61CdYqH"
                
            upbit = pyupbit.Upbit(access_key, screet_key)
            if upbit.get_avg_buy_price(ticker) == 0:
                data_count = 20
                add_average_min_df = self.make_df_add_average_volume(ticker, "minute1", rolling_value=10, count=data_count)
                average_vol = add_average_min_df['average'][data_count-1]
                now_vol = add_average_min_df['volume'][data_count-1]
                
                up_down_value = self.is_up_or_down(add_average_min_df)
                if up_down_value == self.GRAPH_UP:
                    compare_vol = average_vol*7
                    if now_vol >= compare_vol:
                        print('\033[30m', time.strftime('%m-%d %H:%M:%S'), ticker, "구매")                        
                        # buy_log = upbit.buy_market_order(ticker, total_weight)                                                
        except:
            print("error")


class TradeBotCommandDelete(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, param):
        try:
            # find bot by market param
            bot = TradeBotCommand.objects.filter(market=param).update(is_completed=1)            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class TradeBotCommandLog(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:                                    
            logs = TradeBotLogCommand1.objects.all()
            serializer = TradeBotCommandSerializer(logs, many=True)                                                                        
            return Response(serializer.data)                       
        except Exception as e:
            return Response(e)            