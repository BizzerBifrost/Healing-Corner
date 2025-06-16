from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
import json
import pytz
from datetime import datetime, date
from .models import Order

def index(request):
    malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
    today = timezone.now().astimezone(malaysia_tz).date()
    
    # Get today's orders and earnings
    today_orders = Order.objects.filter(created_at__date=today)
    today_earnings = sum(order.total_price for order in today_orders)
    
    # Get all dates with orders for history
    all_dates = Order.objects.dates('created_at', 'day', order='DESC')
    
    # Get all months with orders for monthly history
    all_months = Order.objects.dates('created_at', 'month', order='DESC')
    
    context = {
        'today_orders': today_orders,
        'today_earnings': today_earnings,
        'all_dates': all_dates,
        'all_months': all_months,
    }
    
    return render(request, 'index.html', context)

@require_http_methods(["POST"])
def create_order(request):
    try:
        data = json.loads(request.body)
        
        # Calculate total price
        base_price = Decimal('5.00')
        total_price = base_price
        
        if data.get('add_boba'):
            total_price += Decimal('1.00')
        
        if data.get('cod'):
            total_price += Decimal('1.50')
        
        # Create order
        order = Order.objects.create(
            drink=data['drink'],
            add_boba=data.get('add_boba', False),
            cod=data.get('cod', False),
            recipient_name=data['recipient_name'],
            room_number=data['room_number'],
            location=data['location'],
            total_price=total_price,
            payment_status=data.get('payment_status', 'not_paid')
        )
        
        return JsonResponse({'success': True, 'order_id': order.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_date_orders(request, date_str):
    try:
        # Parse date string (YYYY-MM-DD format)
        from datetime import datetime
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        orders = Order.objects.filter(created_at__date=date)
        total_earnings = sum(order.total_price for order in orders)
        
        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.id,
                'drink': order.get_drink_display(),
                'add_boba': order.add_boba,
                'cod': order.cod,
                'recipient_name': order.recipient_name,
                'room_number': order.room_number,
                'location': order.get_location_display(),
                'total_price': str(order.total_price),
                'payment_status': order.get_payment_status_display(),
                'created_at': order.get_malaysia_time().strftime('%H:%M:%S'),
            })
        
        return JsonResponse({
            'orders': orders_data,
            'total_earnings': str(total_earnings),
            'date': date_str
        })
    
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'})

def get_monthly_earnings(request):
    malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
    current_month = timezone.now().astimezone(malaysia_tz).replace(day=1).date()
    
    monthly_orders = Order.objects.filter(
        created_at__date__gte=current_month
    )
    
    monthly_earnings = sum(order.total_price for order in monthly_orders)
    
    return JsonResponse({
        'monthly_earnings': str(monthly_earnings),
        'month': current_month.strftime('%B %Y')
    })

@require_http_methods(["POST"])
def mark_order_paid(request):
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        
        order = Order.objects.get(id=order_id)
        order.payment_status = 'paid'
        order.save()
        
        return JsonResponse({'success': True})
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Order not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_todays_earnings(request):
    malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
    today = timezone.now().astimezone(malaysia_tz).date()
    
    today_orders = Order.objects.filter(created_at__date=today)
    today_earnings = sum(order.total_price for order in today_orders)
    
    return JsonResponse({
        'today_earnings': f"{today_earnings:.2f}"
    })

def get_month_orders(request, month_str):
    try:
        # Parse month string (YYYY-MM format)
        year, month = month_str.split('-')
        year = int(year)
        month = int(month)
        
        # Get all orders for the specified month
        orders = Order.objects.filter(
            created_at__year=year,
            created_at__month=month
        ).order_by('-created_at')
        
        total_earnings = sum(order.total_price for order in orders)
        
        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.id,
                'drink': order.get_drink_display(),
                'add_boba': order.add_boba,
                'cod': order.cod,
                'recipient_name': order.recipient_name,
                'room_number': order.room_number,
                'location': order.get_location_display(),
                'total_price': str(order.total_price),
                'payment_status': order.get_payment_status_display(),
                'date': order.get_malaysia_time().strftime('%Y-%m-%d'),
                'created_at': order.get_malaysia_time().strftime('%H:%M:%S'),
            })
        
        # Create month name
        month_date = date(year, month, 1)
        month_name = month_date.strftime('%B %Y')
        
        return JsonResponse({
            'orders': orders_data,
            'total_earnings': str(total_earnings),
            'month_name': month_name,
            'month_str': month_str
        })
    
    except (ValueError, IndexError):
        return JsonResponse({'error': 'Invalid month format. Use YYYY-MM'})