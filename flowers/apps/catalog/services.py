from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import register
from apps.cart.forms import CartAddProductForm
from apps.catalog.models import Categories
from apps.products.forms import LoginUserForm
from apps.products.models import Products, Rating


def base_data():
    context = {
        'form': LoginUserForm, 'count': 0,
        'cat': Categories.objects.order_by('date'),
        'cart_product_form': CartAddProductForm()}
    return context


def search_magazine(query):
    context = base_data()
    context['title'] = 'Поиск товара'
    if query is None:
        object_list = Products.objects.all()
    else:
        object_list = Products.objects.filter(Q(title__icontains=query) or Q(slug__icontains=query))
    context['prod'] = object_list
    context.update(get_rating_catalog(context['prod']))
    return context


def magazine_catalog(page_number):
    context = base_data()
    context['cat_selected'] = 0
    prod = Products.objects.order_by('date_created')
    paginator = Paginator(prod, 20)
    context['posts'] = paginator.page(page_number)
    context['prod'] = paginator.get_page(page_number)
    context.update(get_rating_catalog(context['prod']))
    return context


def show_categories(slug):
    context = base_data()
    cater = get_object_or_404(Categories, slug=slug)
    context['prod'] = Products.objects.filter(cat=cater.id).order_by('date_created')
    context['cat_selected'] = cater.id
    context.update(get_rating_catalog(context['prod']))
    return context


def get_rating_catalog(products):
    context = base_data()
    context['prod_rating'] = {}
    for product in products:
        context["prod_rating"].update({product.id: Rating.objects.filter(prod=product).
                                      aggregate(Avg('star')).get('star__avg')})
    return context


@register.filter
def rating(h, key):
    return h[key]
