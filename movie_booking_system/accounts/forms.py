from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'avatar',
            'phone_number',
            'preferred_genre',
            'preferred_language',
            'address',
            'notification_enabled',
            'date_of_birth',
            'profile_picture'
        ]
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_genre': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_language': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notification_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        } 