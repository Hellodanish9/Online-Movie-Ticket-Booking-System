from django.contrib import admin
from .models import Theater, Show

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'total_screens', 'is_active')
    list_filter = ('location', 'is_active')
    search_fields = ('name', 'location')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater', 'screen_number', 'show_date', 'show_time', 'ticket_price', 'available_seats')
    list_filter = ('show_date', 'theater')
    search_fields = ('movie__title', 'theater__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'show_date'
