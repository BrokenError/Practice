from django.shortcuts import render
from django.views.generic import ListView

from apps.catalog.services import search_magazine, show_categories, magazine_catalog
from apps.products.models import Products


class SearchResultView(ListView):
    model = Products
    template_name = 'catalog/search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        query = self.request.GET.get('search_prod')
        context = search_magazine(query)
        return context


def magazine_catalog_view(request):
    page_number = request.GET.get('page', 1)
    context = magazine_catalog(page_number)
    return render(request, 'catalog/catalog.html', context=context)


def show_categories_view(request, slug):
    context = show_categories(slug)
    return render(request, 'catalog/catalog.html', context=context)

