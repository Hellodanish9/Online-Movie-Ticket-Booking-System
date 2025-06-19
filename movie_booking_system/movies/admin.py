from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'duration', 'is_active')
    list_filter = ('genre', 'language', 'is_active')
    search_fields = ('title', 'description', 'genre')
    readonly_fields = ('created_at', 'updated_at')
