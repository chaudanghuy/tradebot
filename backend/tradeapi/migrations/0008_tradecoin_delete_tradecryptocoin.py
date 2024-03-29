# Generated by Django 4.2.9 on 2024-01-23 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradeapi', '0007_tradecryptocoin_delete_tradecrypto'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeCoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('market', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name='TradeCryptoCoin',
        ),
    ]
