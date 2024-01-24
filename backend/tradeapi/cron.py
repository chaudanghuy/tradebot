from .models import TradeBotCommand, TradeBotCommandDetail, TradeBotLogCommand1, TradeBotConfig, TradeBotMyAccount, TradeCoinHistory, TradeBuyBotCommand
import pyupbit
from django.conf import settings

def my_cron_jobs():
    access_key = settings.ACCESS_UPBIT_KEY
    screet_key = settings.SECRET_UPBIT_KEY                
    upbit = pyupbit.Upbit(access_key, screet_key)    
    
    balance = upbit.get_balance("KRW")    
    
    log = TradeBotLogCommand1()
    log.message = 'Log start'
    log.trade_market = ticker
    log.save()
    
    try:
      bots = TradeBuyBotCommand.objects.filter(is_completed=0) 
                
      # loop through bots and check if it is up or down      
      for bot in bots:                          
          ticker = bot.market
          
          if upbit.get_avg_buy_price(ticker) == 0:                            
              data_count = 20
              df = pyupbit.get_ohlcv(ticker, "minute1", 20)
              try:                            
                df = pyupbit.get_ohlcv(ticker, "minute1", count=20)
                df['average'] = df['volume'].rolling(window=10).mean().shift(1)
                add_average_min_df = df
                average_vol = add_average_min_df['average'][data_count-1]
                now_vol = add_average_min_df['volume'][data_count-1]
                
                last_close = add_average_min_df['close'][-1]
                last_open_price = add_average_min_df['open'][-1]                                
                
                # GRAPH_DOWN = 20
                up_down_value = 20
                
                if last_close - last_open_price > 0:                                
                  # GRAPH_UP = 10
                  up_down_value = 10                                                                                                                   
                  
                  if up_down_value == 10:
                    compare_vol = average_vol*5
                    if now_vol >= compare_vol:     
                      bot.is_completed = 1
                      bot.save()           
                      # buy
                      total_weight = balance * bot.trade_volume / 100                                                                            
                      buy_log = upbit.buy_market_order(ticker, total_weight)                                                       
                      print(buy_log)
                      # write TradeBotLogCommand1
                      log = TradeBotLogCommand1()
                      log.message = 'Buy order is completed'
                      log.trade_market = ticker
                      log.save()
              except:                        
                bot.is_completed = 0
                bot.save()                                                                     
    except Exception as e:
      print('Error')
  
         
