from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['recipient_name', 'drink', 'total_price', 'payment_status', 'location', 'created_at']
    list_filter = ['drink', 'payment_status', 'location', 'add_boba', 'cod', 'created_at']
    search_fields = ['recipient_name', 'room_number']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Order Details', {
            'fields': ('drink', 'add_boba', 'cod', 'total_price')
        }),
        ('Customer Information', {
            'fields': ('recipient_name', 'room_number', 'location')
        }),
        ('Payment', {
            'fields': ('payment_status',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )