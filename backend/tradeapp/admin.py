from django.contrib import admin
from .models import Order

# Register your models here.
class TradeAppAdmin(admin.ModelAdmin):
    list_display = ('market', 'side', 'price', 'volume', 'ord_type')
    list_filter = ('market', 'side')
    search_fields = ('market', 'side')

admin.site.register(Order, TradeAppAdmin)