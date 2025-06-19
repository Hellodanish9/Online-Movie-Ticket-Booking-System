from django.urls import path
from . import views

app_name = 'theaters'

urlpatterns = [
    path('', views.theater_list, name='theater_list'),
    path('<int:theater_id>/', views.theater_detail, name='theater_detail'),
    path('<int:theater_id>/shows/', views.theater_shows, name='theater_shows'),
] 