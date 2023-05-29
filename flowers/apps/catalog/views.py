from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import register
from django.views.generic import ListView

from apps.cart.forms import CartAddProductForm
from apps.catalog.models import Categories
from apps.products.forms import LoginUserForm
from apps.products.models import Products, Rating

context = {
    'form': LoginUserForm,
    'count': 0,
    'cat': Categories.objects.order_by('date'),
    'cart_product_form': CartAddProductForm()}


class SearchResultView(ListView):
    model = Products
    template_name = 'catalog/search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context['title'] = 'Поиск товара'
        return context

    def get_queryset(self):
        query = self.request.GET.get('search_prod')
        if query is None:
            object_list = Products.objects.all()
        else:
            object_list = Products.objects.filter(Q(title__icontains=query) or Q(slug__icontains=query))
        context['prod'] = object_list
        return context


def magazine_catalog(request):
    context['cat_selected'] = 0
    prod = Products.objects.order_by('date_created')
    paginator = Paginator(prod, 20)
    page_number = request.GET.get('page', 1)
    context['posts'] = paginator.page(page_number)
    context['prod'] = paginator.get_page(page_number)
    get_rating_catalog(request)
    return render(request, 'catalog/catalog.html', context=context)


def show_categories(request, slug):
    cater = get_object_or_404(Categories, slug=slug)
    context['prod'] = Products.objects.filter(cat=cater.id).order_by('date_created')
    context['cat_selected'] = cater.id
    get_rating_catalog(request)
    return render(request, 'catalog/catalog.html', context=context)


def get_rating_catalog(request):
    context['prod_rating'] = {}
    for i in context['prod']:
        context["prod_rating"].update({i.id: Rating.objects.filter(prod=i).aggregate(Avg('star')).get('star__avg')})
    return context


@register.filter
def rating(h, key):
    return h[key]
