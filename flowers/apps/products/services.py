from django.db.models import Avg
from django.shortcuts import get_object_or_404

from apps.cart.forms import CartAddProductForm
from apps.orders.models import Order
from apps.products.models import Products, Rating


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
    return print(' ')


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
