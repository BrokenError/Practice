from django.contrib.auth.models import User
from django.shortcuts import render

from apps.cart.cart import Cart
from apps.orders.forms import OrderCreateForm
from apps.orders.models import Order, OrderItem


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            obj = Order()
            obj.user = User.objects.get(pk=request.user.id)
            obj.description = form.cleaned_data['description']
            obj.deliv_address = form.cleaned_data['deliv_address']
            obj.paid = form.cleaned_data['paid']
            obj.save()

            for item in cart:
                OrderItem.objects.create(
                    order=obj,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/order/creation.html', {'order': obj})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
