from django.db import models
from django.conf import settings
from theaters.models import Show

class BookingCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='booking_carts')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='booking_carts')
    seat_numbers = models.CharField(max_length=255, help_text="Comma separated seat numbers")
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.username} - {self.show} - {self.number_of_seats} seats"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    number_of_seats = models.PositiveIntegerField()
    seat_numbers = models.CharField(max_length=255, help_text="Comma separated seat numbers")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.show}"

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
        ('net_banking', 'Net Banking'),
    )
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.amount}"

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('generated', 'Generated'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
    )
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='invoice')
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='invoice')
    invoice_date = models.DateTimeField(auto_now_add=True)
    invoice_number = models.CharField(max_length=50, unique=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='generated')
    
    def __str__(self):
        return f"Invoice {self.invoice_number} for Booking {self.booking.id}"
