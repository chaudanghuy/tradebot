from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from upbit.client import Upbit
from django.contrib.auth.decorators import login_required
from .forms import CryptoSearchForm
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Order, BotCoin

# Create your views here.
@login_required(login_url="/accounts/login/")
def index(request):
     access_key = settings.ACCESS_KEY
     secret_key = settings.SECRET_KEY
     form = CryptoSearchForm(request.GET)
     upbit = Upbit(access_key, secret_key)
     account = upbit.Account.Account_wallet()
     coins = upbit.Market.Market_info_all()
     orderbooks = upbit.Order.Order_orderbook(
          markets=['KRW-BTC']
     )
     return render(request, 'tradeapp/index.html', 
                   {
                        'account': account['result'],
                        'coins': coins['result'], 
                        'form': form,
                        'orderbooks': orderbooks['result']
                    }
               )
     
@login_required(login_url="/accounts/login/")     
def get_order_book(request):
     access_key = settings.ACCESS_KEY
     secret_key = settings.SECRET_KEY
     coin = request.GET['coin']
     upbit = Upbit(access_key, secret_key)
     orderbooks = upbit.Order.Order_orderbook(
          markets=[coin]
     )
     return HttpResponse(json.dumps(orderbooks['result']))

@login_required(login_url="/accounts/login/") 
def get_coin_price(request):
     access_key = settings.ACCESS_KEY
     secret_key = settings.SECRET_KEY
     coin = request.GET['coin']
     upbit = Upbit(access_key, secret_key)
     resp = upbit.Candle.Candle_minutes(
          unit=1,
          market=coin
     )
     return HttpResponse(json.dumps(resp['result']))

@login_required(login_url="/accounts/login/") 
@csrf_exempt
def create_order(request):
     if request.method == 'POST':
        try:             
            data = json.loads(request.body)                               
            market = data.get('market')
            side = data.get('side')
            volume = data.get('volume')
            price = data.get('price')
            ord_type = data.get('ord_type')

            order = Order.objects.create(market=market, side=side, volume=volume, price=price, ord_type=ord_type)
            return JsonResponse({'market': market, 'volume': volume, 'price': price})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)    
       
def order_list(request):
    orders = Order.objects.all().order_by('-id')
    order_list = [{'market': order.market, 'side': order.side, 'volume': order.volume,'price': order.price,'ord_type': order.ord_type} for order in orders]
    return JsonResponse({'orders': order_list})

@csrf_exempt
def create_bot(request):
     if request.method == 'POST':
          try:             
               data = json.loads(request.body)                               
               market = data.get('market')
               total_volume = data.get('total_volume')
               profit_rate = data.get('profit_rate')
     
               botcoin = BotCoin.objects.create(market=market, total_volume=total_volume, profit_rate=profit_rate)
               return JsonResponse({'market': market, 'total_volume': total_volume, 'profit_rate': profit_rate})
          except Exception as e:
               return JsonResponse({'error': str(e)}, status=400)          