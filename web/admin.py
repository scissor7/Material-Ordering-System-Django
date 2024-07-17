from django.contrib import admin
from web import models


class MerchAdmin(admin.ModelAdmin):
    list_display = ['title','price','num','broker']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['title','num','buyer','broker','order_time']


class DemandAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'num','buyer']


admin.site.register(models.Merch,MerchAdmin)
admin.site.register(models.Order,OrderAdmin)
admin.site.register(models.Demand,DemandAdmin)
