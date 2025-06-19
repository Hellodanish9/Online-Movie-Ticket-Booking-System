from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm, UserProfileForm, UserInfoForm
from django.utils import timezone
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@require_http_methods(["GET", "POST"])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully!")
    return redirect('movies:movie_list')

@login_required
def profile_view(request):
    # Ensure profile exists
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    edit_mode = request.GET.get('edit', False)
    
    if request.method == 'POST':
        user_form = UserInfoForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user_form.save()
                profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserInfoForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'edit_mode': edit_mode,
        'active_bookings': request.user.bookings.filter(show__show_date__gte=timezone.now().date()).order_by('show__show_date', 'show__show_time')[:5]
    }
    return render(request, 'accounts/profile.html', context)
