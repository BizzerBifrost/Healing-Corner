from django.db import models
from django.utils import timezone
import pytz

class Order(models.Model):
    DRINK_CHOICES = [
        ('green_tea', 'Green Tea'),
        ('chocolate', 'Chocolate'),
        ('latte', 'Latte'),
    ]
    
    LOCATION_CHOICES = [
        ('idaman', 'Idaman'),
        ('ilham', 'Ilham'),
        ('impian', 'Impian'),
        ('psn', 'PSN'),
        ('surau', 'Surau'),
        ('cafe', 'Cafe'),
        ('self_pickup', 'Self-Pickup'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('not_paid', 'Not Paid'),
    ]
    
    drink = models.CharField(max_length=20, choices=DRINK_CHOICES)
    add_boba = models.BooleanField(default=False)
    cod = models.BooleanField(default=False)
    recipient_name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='not_paid')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recipient_name} - {self.get_drink_display()} - RM{self.total_price}"
    
    def get_malaysia_time(self):
        malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
        return self.created_at.astimezone(malaysia_tz)
    
    @classmethod
    def get_today_orders(cls):
        malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
        today = timezone.now().astimezone(malaysia_tz).date()
        return cls.objects.filter(created_at__date=today)
    
    @classmethod
    def get_today_earnings(cls):
        today_orders = cls.get_today_orders()
        return sum(order.total_price for order in today_orders)