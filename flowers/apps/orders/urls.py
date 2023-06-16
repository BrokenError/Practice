from django.urls import path

from apps.orders.views import create_order_view, paid_order_view

urlpatterns = [path('create/', create_order_view, name='order_create'),
               path('paid-order/', paid_order_view, name='paid_order'),
               ]
