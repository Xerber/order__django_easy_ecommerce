from django.contrib import admin
from cart.models import *


# Register your models here.
class OrderItemInline(admin.TabularInline):
    '''Товары к заказам'''
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Заказы'''
    list_display = ("order_id","first_name","address","phone","email","total_amount","status")
    list_editable = ("status",)
    readonly_fields = ("order_id","first_name","last_name","address","add_address","phone","email","total_amount","cart_data")
    list_filter = ("id","first_name","phone","status")
    search_fields = ("first_name","address","phone")
    inlines = [OrderItemInline,]
