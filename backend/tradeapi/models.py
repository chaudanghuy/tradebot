from django.db import models

# Create your models here.
class TradeBotCommand(models.Model):
    market = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)    
    trade_price = models.FloatField()
    trade_volume = models.FloatField()
    ask_bid = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    
class TradeBotCommandDetail(models.Model):
    command = models.ForeignKey(TradeBotCommand, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    profit_rate = models.FloatField()
    transaction_volume_rate = models.FloatField()
    trade_price = models.FloatField()
    trade_volume = models.FloatField()
    compare_data_count = models.CharField(max_length=100)
    rolling_data_count = models.CharField(max_length=100)
    ask_bid = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)    

class TradeBotLogCommand(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=100)
    is_error = models.BooleanField(default=False)
    trade_bot = models.ForeignKey(TradeBotCommandDetail, on_delete=models.CASCADE)    

class TradeBotConfig(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class TradeBotMyAccount(models.Model):
    market = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    balance = models.FloatField()
    avg_buy_price = models.FloatField()
    avg_buy_price_modified = models.BooleanField(default=False)
    unit_currency = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

class TradeCoinHistory(models.Model):
    market = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    trade_price = models.FloatField()
    trade_volume = models.FloatField()
    ask_bid = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    
class TradeBotSetting(models.Model):
    accessKey = models.CharField(max_length=200)
    secretKey = models.CharField(max_length=200)
    currency = models.CharField(max_length=10)
    time_sleep = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)    