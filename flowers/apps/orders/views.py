from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from apps.cart.cart import Cart
from apps.orders.forms import OrderCreateForm
from apps.orders.services import order_create


@login_required
def create_order_view(request):
    return render(request, 'orders/order/create.html', {'cart': Cart(request), 'form': OrderCreateForm})


@login_required
@require_http_methods(['POST'])
def paid_order_view(request):
    result = order_create(request.method, Cart(request), OrderCreateForm(request.POST), request.user)
    return render(request, 'orders/order/creation.html', {'result': result})
