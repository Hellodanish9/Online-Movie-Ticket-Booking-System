# Generated by Django 5.2 on 2025-05-16 17:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('theaters', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('number_of_seats', models.PositiveIntegerField()),
                ('seat_numbers', models.CharField(help_text='Comma separated seat numbers', max_length=255)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('booking_status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=10)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='theaters.show')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_numbers', models.CharField(help_text='Comma separated seat numbers', max_length=255)),
                ('number_of_seats', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_carts', to='theaters.show')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_carts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(choices=[('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('upi', 'UPI'), ('net_banking', 'Net Banking')], max_length=20)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending', max_length=10)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='bookings.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_date', models.DateTimeField(auto_now_add=True)),
                ('invoice_number', models.CharField(max_length=50, unique=True)),
                ('tax_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice_status', models.CharField(choices=[('generated', 'Generated'), ('sent', 'Sent'), ('viewed', 'Viewed')], default='generated', max_length=10)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='bookings.booking')),
                ('payment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='bookings.payment')),
            ],
        ),
    ]
