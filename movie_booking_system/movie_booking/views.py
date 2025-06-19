from django.shortcuts import render
from movies.models import Movie

def home(request):
    movies = Movie.objects.filter(is_active=True)[:6]
    return render(request, 'home.html', {'movies': movies}) 