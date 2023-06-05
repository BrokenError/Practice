from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from apps.cart.cart import Cart
from apps.cart.forms import CartAddProductForm
from apps.orders.models import Order
from apps.products.models import Products
from apps.user.models import UserLike
from apps.catalog.views import get_rating_catalog


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})


class MoreInfo(ListView):
    model = Order
    template_name = 'cart/history-orders.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {'title': 'История заказов'}
        orders = Order.objects.filter(user_id=self.request.user.id).order_by('created')[:20]
        paginator = Paginator(orders, 10)
        page_number = self.request.GET.get('page', 1)
        context['posts'] = paginator.page(page_number)
        context['orders'] = paginator.get_page(page_number)
        return context


class LikedPages(ListView):
    model = UserLike
    template_name = 'cart/liked.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Понравившиеся товары'
        context['products'] = Products.objects.filter(check_like__user=self.request.user)
        context.update(get_rating_catalog(self.request, context['products']))
        paginator = Paginator(context['products'], 20)
        page_number = self.request.GET.get('page', 1)
        context['page'] = paginator.page(page_number)
        context['products'] = paginator.get_page(page_number)
        return context
        
