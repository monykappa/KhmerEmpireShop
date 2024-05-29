from django.contrib import admin
from orders.models import *
from products.models import *
# Register your models here.
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(OrderHistory)
admin.site.register(OrderHistoryItem)