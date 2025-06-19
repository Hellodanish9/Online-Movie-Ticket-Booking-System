from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
    path('theaters/', include('theaters.urls')),
    path('bookings/', include('bookings.urls')),
    path('accounts/', include('accounts.urls')),  # Include all accounts URLs
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='movies:movie_list'), name='logout'),
    path('register/', account_views.register, name='register'),
] 