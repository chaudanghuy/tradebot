from django.db import models

# Create your models here.
class CryptoAccount(models.Model):
     username = models.CharField(max_length=100)
     balance = models.DecimalField(max_digits=20, decimal_places=10)
     
     
class CryptoCurrency(models.Model):
     name = models.CharField(max_length=100)
     symbol = models.CharField(max_length=10)
     price = models.DecimalField(max_digits=20, decimal_places=10)