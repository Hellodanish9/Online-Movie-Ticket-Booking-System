from django.contrib import admin
from .models import BookingCart, Booking, Payment, Invoice

@admin.register(BookingCart)
class BookingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'number_of_seats', 'total_price', 'created_at', 'expires_at')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('user__username', 'show__movie__title')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'show', 'booking_date', 'number_of_seats', 'total_amount', 'booking_status')
    list_filter = ('booking_status', 'booking_date')
    search_fields = ('user__username', 'show__movie__title')
    readonly_fields = ('booking_date',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_date', 'payment_method', 'status')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('booking__user__username', 'transaction_id')
    readonly_fields = ('payment_date',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'booking', 'invoice_date', 'total_amount', 'invoice_status')
    list_filter = ('invoice_status', 'invoice_date')
    search_fields = ('invoice_number', 'booking__user__username')
    readonly_fields = ('invoice_date',)
