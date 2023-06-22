import requests
from bs4 import BeautifulSoup
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from apps.cart.forms import CartAddProductForm
from apps.orders.models import Order
from apps.products.models import Products, Rating
from apps.products.forms import LoginUserForm


def base_context(self, context):
    product = get_object_or_404(Products, slug=self.kwargs['prod_slug'])
    user_orders = Order.objects.filter(user_id=self.request.user.id)
    context['stars'] = Rating.objects.filter(prod=product.id).aggregate(Avg('star')).get('star__avg')
    context['product_paid'] = False
    context['check_like'] = product.check_like.filter(user_id=self.request.user.id, product=product).exists()
    check_buy = user_orders.filter(linkorder__product_id=product.id)
    check_not_review = not product.check_review.filter(user=self.request.user.id).exists()
    if check_buy:
        context['product_paid'] = True
    context.update({'product': product, 'star': [1, 2, 3, 4, 5],
                    'cart_product_form': CartAddProductForm(), 'check_not_review': check_not_review})
    return context


def grade_product(user, grade):
    user_grade = str(grade).split()
    prod = Products.objects.get(id=user_grade[1])
    update_for = {'user': user, 'star': user_grade[0]}
    Rating.objects.update_or_create(user=user, prod=prod, defaults=update_for)


def fill_form(form, product, user):
    if form.is_valid():
        forme = form.save(commit=False)
        forme.user = user
        forme.product = product
        forme.save()


def change_writes(model, check_id, product_id):
    check_write = model.objects.filter(id=check_id).filter(product_id=product_id)
    return check_write


def change_comment(product_id, check_id, model, form):
    form.save(commit=False)
    result = change_writes(model, check_id, product_id)
    if result.exists():
        result.update(text=form.cleaned_data['text'])


def change_review(product_id, check_id, model, form):
    form.save(commit=False)
    result = change_writes(model, check_id, product_id)
    if result.exists():
        result.update(text=form.cleaned_data['text'], name=form.cleaned_data['name'])


def change_reply_comment(product_id, check_id, model, form, comment_id):
    form.save(commit=False)
    result = change_writes(model, check_id, product_id).filter(comment_id=comment_id)
    result.update(text=form.cleaned_data['text'])


def show_our_stores(answer, ip):
    data = {'Rostov-on-Don': '%3A7187d1900e8f6fb609fd28593c8d2689135091c7e8c6aeb846b43b29deaa3210',
            'Moscow': '%3A6ba45ccc3778f11ab04a791350f71a03b7c87332aab7ed5b3d57470f564adbee',
            'Voronesh': '%3A1688495215b83856fbb37d8a1a91c4edc25e1d6a237d6933c11312a6ab6ea2f1',
            'Volgograd': '%3A28fcedf564921587da2e057ae0884202359b077cea124b0b68941958eeb941f3',
            'country': '%3A6a027cc11bee21604b8a97e648e09535306806441f0b71ec2a00e67d522cc289'}
    page = requests.get(f'https://check-host.net/ip-info?host={ip}')
    soup = BeautifulSoup(page.text, 'html.parser')

    location = soup.findAll('table', class_='hostinfo result')
    data_user = str(location[1].text).replace('\n', ' ').split('  ')
    country = data_user[10]
    city = data_user[15]
    if not answer or f"{city}" not in data.keys():
        map_code = data['country']
    else:
        map_code = data[f"{city}"]
    context = {'title': 'Наши магазины', 'form': LoginUserForm, 'ip': ip, 'location': f'{country} {city}',
               'map_code': map_code, 'answer': answer}
    return context
