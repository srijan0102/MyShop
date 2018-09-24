from django.contrib import admin
from shop.models import Category, Product

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']  # edit multiple rows at once, must be in list_display list
    prepopulated_fields = {'slug': ('name',)}  # specify fields whether value is save using the value of other field


admin.site.register(Product, ProductAdmin)
