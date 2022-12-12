from django.contrib import admin
from .models import Review, Category, Product, Color, Image

admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Image)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "stars", "time_create"]
    readonly_fields = ["stars", ]
    search_fields = ["name_istartswith", ]
    list_filter = ("stars", "time_create")
    list_per_page = 10


class ColorInline(admin.TabularInline):
    model = Color


class ImageInline(admin.TabularInline):
    model = Image


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ColorInline, ImageInline]
    list_display = ["name", 'category', 'price', 'time_create', "visits", "size"]
    search_fields = ["name__istartswith", "category__name"]
    readonly_fields = ["visits", ]
    list_editable = ["price", "size", "category"]
    list_filter = ("price", "time_create")
    list_per_page = 20

