# Generated by Django 4.2.9 on 2024-01-23 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradeapi', '0006_rename_tradecoin_tradecrypto'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeCryptoCoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('market', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='TradeCrypto',
        ),
    ]
