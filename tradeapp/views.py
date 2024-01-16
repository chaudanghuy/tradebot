from django.shortcuts import render
from django.http import HttpResponse
from upbit.client import Upbit
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/accounts/login/")
def index(request):
     access_key = "6j9pBvExB9jWxVwgZb8I6JcsGtOqVSdUUOCNeGBQ"
     secret_key = "2bxUSMoljgnR6c5OhImHUtpJoWH6LY7nF61CdYqH"
     upbit = Upbit(access_key, secret_key)
     balance = upbit.Account.Account_info()
     return render(request, 'tradeapp/index.html', {'balance': balance['result']})