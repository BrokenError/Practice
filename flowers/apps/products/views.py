from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from apps.catalog.models import Products, Rating, RatingStar
from apps.orders.models import Order


def about_us(request):
    context = {'title': 'О нас'}
    return render(request, 'products/aboutus.html', context=context)


def show_product(request, prod_slug):
    context = {'product_paid':False}
    ids = []
    product = get_object_or_404(Products, slug=prod_slug)
    context['product'] = Products.objects.get(pk=product.id)
    context['prod_name'] = product.title
    quantity_star = Rating.objects.filter(movie=product.id).count()
    star = Rating.objects.filter(movie=product.id).values_list('star', flat=True)
    if quantity_star > 0:
        context['stars'] = sum(star)/quantity_star
    items = list(Order.objects.filter(user_id=request.user.id))
    for i in items:
        i.linkorder.all()
        for j in list(i.linkorder.all()):
            ids.append(str(j).split()[0])
    if f'{product.id}' in ids:
        context['product_paid'] = True

    return render(request, 'catalog/product.html', context=context)


def grade_product(request):
    grade = request.GET.get('grade_product')
    user_grade = str(grade).split()
    print(user_grade[1])
    star = RatingStar.objects.get(value=user_grade[0])
    prod = Products.objects.get(id=user_grade[1])
    rec = Rating.objects.create(ip='fff', user=request.user, star=star, movie=prod)
    rec.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
