from django.contrib import admin
from .models import Product, OrderProduct, Order, OrderInfo, Image


class OrderInfoInline(admin.TabularInline):
    model = OrderInfo
    max_num = 1


class OrderProductInline(admin.StackedInline):
    model = OrderProduct
    readonly_fields = ('price', )


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'data', 'status', )
    inlines = [OrderProductInline, OrderInfoInline, ]
    readonly_fields = ('data', )


admin.site.register(Order, OrderProductAdmin)