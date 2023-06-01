from django.contrib import admin

from apps.catalog.models import Categories


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'date']
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}
