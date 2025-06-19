from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'bookings'

# Add a function to redirect to my_bookings
def redirect_to_my_bookings(request):
    return redirect('bookings:my_bookings')

urlpatterns = [
    # Add the base URL pattern that redirects to my-bookings
    path('', redirect_to_my_bookings, name='bookings_home'),
    path('show/<int:show_id>/seats/', views.select_seats, name='select_seats'),
    path('show/<int:show_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
] 