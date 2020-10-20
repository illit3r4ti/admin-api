from django.contrib import admin
from .models import Order, Retailer, Supplier, Concession, Memo, ManualOrder

admin.site.register(Order)
admin.site.register(Retailer)
admin.site.register(Supplier)
admin.site.register(Concession)
admin.site.register(Memo)
admin.site.register(ManualOrder)