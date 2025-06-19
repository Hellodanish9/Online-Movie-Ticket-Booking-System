from django.shortcuts import render, get_object_or_404
from .models import Movie
from theaters.models import Show
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse

def movie_list(request):
    movies = Movie.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    language = request.GET.get('language', '')
    genre = request.GET.get('genre', '')
    format_type = request.GET.get('format', '')
    
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if language and language != 'All Languages':
        movies = movies.filter(language=language)
        
    if genre and genre != 'All Genres':
        movies = movies.filter(genre=genre)
    
    # Get unique languages and genres for filters
    all_languages = list(sorted(set(Movie.objects.filter(is_active=True).values_list('language', flat=True))))
    all_genres = list(sorted(set(Movie.objects.filter(is_active=True).values_list('genre', flat=True))))
    
    context = {
        'movies': movies,
        'search_query': search_query,
        'selected_language': language,
        'selected_genre': genre,
        'selected_format': format_type,
        'all_languages': all_languages,
        'all_genres': all_genres
    }
    
    return render(request, 'movies/movie_list.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id, is_active=True)
    shows = Show.objects.filter(
        movie=movie,
        show_date__gte=timezone.now().date()
    ).order_by('show_date', 'show_time')
    
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'shows': shows
    })

def movie_suggestions(request):
    """API endpoint to get movie suggestions for autocomplete"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query),
            is_active=True
        )[:8]  # Limit to 8 suggestions
        
        results = [
            {
                'id': movie.id,
                'title': movie.title,
                'genre': movie.genre,
                'language': movie.language,
                'poster_url': movie.poster_image.url if movie.poster_image else None,
            }
            for movie in movies
        ]
    
    return JsonResponse({'results': results})
