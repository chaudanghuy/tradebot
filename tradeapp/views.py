from django.shortcuts import render
from django.http import HttpResponse
from upbit.client import Upbit
from django.contrib.auth.decorators import login_required
from .forms import CryptoSearchForm
from django.conf import settings

# Create your views here.
@login_required(login_url="/accounts/login/")
def index(request):
     access_key = settings.ACCESS_KEY
     secret_key = settings.SECRET_KEY
     form = CryptoSearchForm(request.GET)
     upbit = Upbit(access_key, secret_key)
     account = upbit.Account.Account_info()
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