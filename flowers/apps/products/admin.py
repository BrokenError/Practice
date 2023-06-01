from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.products.models import Products, Reviews, Comments


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'image_show', 'price', 'available', 'date_created', 'date_uploaded']
    list_filter = ['available', 'date_created', 'date_uploaded']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('title',)}

    def image_show(self, obj):
        if obj.photo:
            return mark_safe("<img src='{}' width='50' />".format(obj.photo.url))
        return 'None'

    image_show.__name__ = "Картинка"

    
@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'text', 'product', 'date_created', 'date_uploaded']
    list_filter = ['id', 'date_created', 'date_uploaded']


@admin.register(Comments)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'text', 'product', 'date']
    list_filter = ['id', 'user']
    