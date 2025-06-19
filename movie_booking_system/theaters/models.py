from django.db import models
from django.conf import settings
from movies.models import Movie

class Theater(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    total_screens = models.PositiveIntegerField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='added_theaters')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.location}"

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='shows')
    screen_number = models.PositiveIntegerField()
    show_date = models.DateField()
    show_time = models.TimeField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='added_shows')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.movie.title} - {self.theater.name} - {self.show_date} {self.show_time}"
    
    class Meta:
        ordering = ['show_date', 'show_time']
        unique_together = ('theater', 'screen_number', 'show_date', 'show_time')
