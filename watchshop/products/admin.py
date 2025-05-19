from django.contrib import admin
from .models import Watch, Brand

@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'watch_type', 'in_stock')
    list_filter = ('brand', 'watch_type', 'in_stock')
    search_fields = ('name', 'description')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)