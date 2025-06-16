from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-order/', views.create_order, name='create_order'),
    path('date-orders/<str:date_str>/', views.get_date_orders, name='date_orders'),
    path('month-orders/<str:month_str>/', views.get_month_orders, name='month_orders'),
    path('monthly-earnings/', views.get_monthly_earnings, name='monthly_earnings'),
    path('mark-paid/', views.mark_order_paid, name='mark_paid'),
    path('todays-earnings/', views.get_todays_earnings, name='todays_earnings'),
]