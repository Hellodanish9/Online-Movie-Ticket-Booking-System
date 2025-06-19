from django.utils import timezone
from .models import BookingCart

def cart_count(request):
    if request.user.is_authenticated:
        count = BookingCart.objects.filter(
            user=request.user,
            expires_at__gt=timezone.now()
        ).count()
        return {'cart_count': count}
    return {'cart_count': 0} 