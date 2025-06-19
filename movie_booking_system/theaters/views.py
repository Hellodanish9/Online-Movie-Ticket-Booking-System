from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Theater, Show

def theater_list(request):
    theaters = Theater.objects.all()
    return render(request, 'theaters/theater_list.html', {'theaters': theaters})

def theater_detail(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    today = timezone.now().date()
    
    # Get upcoming shows for this theater
    upcoming_shows = Show.objects.filter(
        theater=theater,
        show_date__gte=today
    ).order_by('show_date', 'show_time')
    
    return render(request, 'theaters/theater_detail.html', {
        'theater': theater,
        'upcoming_shows': upcoming_shows
    })

def theater_shows(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    today = timezone.now().date()
    
    # Get all shows for this theater
    shows = Show.objects.filter(
        theater=theater,
        show_date__gte=today
    ).order_by('show_date', 'show_time')
    
    return render(request, 'theaters/theater_shows.html', {
        'theater': theater,
        'shows': shows
    })
