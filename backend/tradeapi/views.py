from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import TradeapiSerializer
from .models import TradeBot, TradeBotLog, TradeBotConfig, TradeBotMyAccount, TradeCoinHistory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from upbit.client import Upbit

# Create your views here.
class TradeapiView(viewsets.ModelViewSet):
    serializer_class = TradeapiSerializer
    queryset = TradeBot.objects.all()
    
class TradeBotView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Welcome to the JWT authentication page using React and Django'}
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
            
            client = Upbit(access_key, screet_key)
            api_keys = client.APIKey.APIKey_info()
            return Response(api_keys)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)        