from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from apps.catalog.services import get_rating_catalog
from apps.orders.models import Order
from apps.products.models import Products
from apps.cart.forms import CartAddProductForm


def add_product_in_cart(cart, form, product_id):
    product = get_object_or_404(Products, id=product_id)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])


def delete_product_from_cart(cart, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)


def update_quantity(cart):
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return cart


def liked_products(context, user, page_number):
    context['title'] = 'Понравившиеся товары'
    context['products'] = Products.objects.filter(check_like__user=user)
    context.update(get_rating_catalog(context['products']))
    paginator = Paginator(context['products'], 20)
    context['page'] = paginator.page(page_number)
    context['products'] = paginator.get_page(page_number)
    return context


def history_orders(context, user_id, page_number):
    context.update({'title': 'История заказов'})
    orders = Order.objects.filter(user_id=user_id).order_by('-created')[:20]
    paginator = Paginator(orders, 10)
    context['posts'] = paginator.page(page_number)
    context['orders'] = paginator.get_page(page_number)
    return context
