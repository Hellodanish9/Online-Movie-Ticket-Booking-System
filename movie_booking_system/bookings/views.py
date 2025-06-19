from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from theaters.models import Show
from .models import BookingCart, Booking, Payment, Invoice
import uuid
import random
from django.urls import reverse

@login_required
def select_seats(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    
    # Check if show date is in the past
    if show.show_date < timezone.now().date():
        messages.error(request, "This show has already passed.")
        return redirect('movies:movie_detail', movie_id=show.movie.id)
    
    # Get all current bookings for this show to mark seats as taken
    bookings = Booking.objects.filter(show=show, booking_status__in=['confirmed', 'pending'])
    booked_seats = []
    
    for booking in bookings:
        seats = booking.seat_numbers.split(',')
        booked_seats.extend(seats)
    
    # Total rows and seats per row (simplified for demo)
    total_rows = 8
    seats_per_row = 10
    
    context = {
        'show': show,
        'booked_seats': booked_seats,
        'total_rows': total_rows,
        'seats_per_row': seats_per_row,
        'rows': range(1, total_rows + 1),
        'seats': range(1, seats_per_row + 1),
    }
    
    return render(request, 'bookings/select_seats.html', context)

@login_required
def add_to_cart(request, show_id):
    if request.method == 'POST':
        show = get_object_or_404(Show, id=show_id)
        selected_seats = request.POST.getlist('seats')
        
        if not selected_seats:
            messages.error(request, "Please select at least one seat.")
            return redirect('bookings:select_seats', show_id=show_id)
        
        # Check if seats are already booked
        bookings = Booking.objects.filter(show=show, booking_status__in=['confirmed', 'pending'])
        booked_seats = []
        
        for booking in bookings:
            seats = booking.seat_numbers.split(',')
            booked_seats.extend(seats)
        
        # Check if any selected seat is already booked
        if any(seat in booked_seats for seat in selected_seats):
            messages.error(request, "Some selected seats are already booked. Please choose different seats.")
            return redirect('bookings:select_seats', show_id=show_id)
        
        # Clear existing cart items for this user and show
        BookingCart.objects.filter(user=request.user, show=show).delete()
        
        # Create new cart
        seat_numbers = ','.join(selected_seats)
        number_of_seats = len(selected_seats)
        total_price = number_of_seats * show.ticket_price
        
        # Cart expires in 10 minutes
        expires_at = timezone.now() + timedelta(minutes=10)
        
        cart = BookingCart.objects.create(
            user=request.user,
            show=show,
            seat_numbers=seat_numbers,
            number_of_seats=number_of_seats,
            total_price=total_price,
            expires_at=expires_at
        )
        
        messages.success(
            request,
            f'Added {number_of_seats} seat(s) to cart: {seat_numbers}. '
            f'<a href="{reverse("bookings:cart")}">View Cart</a> '
            f'(expires in 10 minutes)',
            extra_tags='safe'
        )
        
        # Get other cart items
        other_cart_items = BookingCart.objects.filter(
            user=request.user,
            expires_at__gt=timezone.now()
        ).exclude(id=cart.id)
        
        if other_cart_items.exists():
            messages.info(
                request,
                f'You have {other_cart_items.count()} other item(s) in your cart. '
                f'<a href="{reverse("bookings:cart")}">View All</a>',
                extra_tags='safe'
            )
        
        return redirect('bookings:cart')
    
    return redirect('bookings:select_seats', show_id=show_id)

@login_required
def cart(request):
    # Get current cart items that haven't expired
    cart_items = BookingCart.objects.filter(
        user=request.user,
        expires_at__gt=timezone.now()
    )
    
    total_amount = sum(item.total_price for item in cart_items)
    
    return render(request, 'bookings/cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })

@login_required
def checkout(request):
    # Get current cart items that haven't expired
    cart_items = BookingCart.objects.filter(
        user=request.user,
        expires_at__gt=timezone.now()
    )
    
    if not cart_items:
        messages.error(request, "Your cart is empty or has expired.")
        return redirect('bookings:cart')
    
    total_amount = sum(item.total_price for item in cart_items)
    
    return render(request, 'bookings/checkout.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })

@login_required
def process_payment(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        # Get current cart items that haven't expired
        cart_items = BookingCart.objects.filter(
            user=request.user,
            expires_at__gt=timezone.now()
        )
        
        if not cart_items:
            messages.error(request, "Your cart is empty or has expired.")
            return redirect('bookings:cart')
        
        # Process each cart item as a booking
        for cart_item in cart_items:
            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                show=cart_item.show,
                booking_date=timezone.now(),
                number_of_seats=cart_item.number_of_seats,
                seat_numbers=cart_item.seat_numbers,
                total_amount=cart_item.total_price,
                booking_status='confirmed'
            )
            
            # Create payment
            transaction_id = f"TXN{uuid.uuid4().hex[:8].upper()}"
            payment = Payment.objects.create(
                booking=booking,
                amount=cart_item.total_price,
                payment_date=timezone.now(),
                payment_method=payment_method,
                transaction_id=transaction_id,
                status='success'
            )
            
            # Create invoice with proper Decimal calculation
            invoice_number = f"INV{timezone.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
            tax_amount = cart_item.total_price * Decimal('0.18')  # 18% GST
            total_with_tax = cart_item.total_price + tax_amount
            
            Invoice.objects.create(
                booking=booking,
                payment=payment,
                invoice_date=timezone.now(),
                invoice_number=invoice_number,
                tax_amount=tax_amount,
                total_amount=total_with_tax,
                invoice_status='generated'
            )
            
            # Update show's available seats
            cart_item.show.available_seats -= cart_item.number_of_seats
            cart_item.show.save()
            
            # Delete cart item
            cart_item.delete()
        
        messages.success(request, "Payment successful! Your tickets have been booked.")
        return redirect('bookings:confirmation')
    
    return redirect('bookings:checkout')

@login_required
def confirmation(request):
    # Get latest booking
    latest_booking = Booking.objects.filter(
        user=request.user,
        booking_status='confirmed'
    ).order_by('-booking_date').first()
    
    if not latest_booking:
        messages.error(request, "No recent bookings found.")
        return redirect('accounts:profile')
    
    return render(request, 'bookings/confirmation.html', {
        'booking': latest_booking
    })

@login_required
def my_bookings(request):
    # Get current date
    today = timezone.now().date()
    
    # Get upcoming bookings (shows that haven't happened yet)
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        show__show_date__gte=today
    ).order_by('show__show_date', 'show__show_time')
    
    # Get past bookings (shows that have already happened)
    past_bookings = Booking.objects.filter(
        user=request.user,
        show__show_date__lt=today
    ).order_by('-show__show_date', '-show__show_time')
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
    }
    
    return render(request, 'bookings/my_bookings.html', context)

@login_required
def booking_detail(request, booking_id):
    booking = Booking.objects.get(id=booking_id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    if request.method == 'POST':
        booking = Booking.objects.get(id=booking_id, user=request.user)
        
        # Only allow cancellation of confirmed bookings for future shows
        if booking.status == 'confirmed' and booking.show.show_date >= timezone.now().date():
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Your booking has been cancelled successfully.')
        else:
            messages.error(request, 'This booking cannot be cancelled.')
    
    return redirect('bookings:my_bookings')
