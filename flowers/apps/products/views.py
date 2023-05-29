from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from apps.cart.forms import CartAddProductForm
from apps.orders.models import Order
from apps.products.models import Products, Rating, RatingStar


def about_us(request):
    context = {'title': 'О нас'}
    return render(request, 'products/aboutus.html', context=context)


def show_product(request, prod_slug):
    context = {'product_paid': False}
    ids = []
    product = get_object_or_404(Products, slug=prod_slug)
    context['product'] = product
    context['prod_name'] = product.title
    quantity_star = Rating.objects.filter(prod=product.id).count()
    star = Rating.objects.filter(prod=product.id).values_list('star', flat=True)
    if quantity_star > 0:
        context['stars'] = sum(star)/quantity_star
    items = list(Order.objects.filter(user_id=request.user.id))
    for i in items:
        i.linkorder.all()
        for j in list(i.linkorder.all()):
            ids.append(str(j).split()[0])
    if f'{product.id}' in ids:
        context['product_paid'] = True
    context['cart_product_form'] = CartAddProductForm()
    context['star'] = [1, 2, 3, 4, 5]
    return render(request, 'products/product.html', context=context)


def grade_product(request):
    grade = request.GET.get('grade_product')
    user_grade = str(grade).split()
    star = RatingStar.objects.get(value=user_grade[0])
    prod = Products.objects.get(id=user_grade[1])
    update_for = {'user': request.user, 'star': star, 'prod': prod}
    Rating.objects.update_or_create(user=request.user, defaults=update_for)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
