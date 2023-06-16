from django.urls import path

from apps.catalog.views import magazine_catalog_view, show_categories_view, SearchResultView

urlpatterns = [
    path('', magazine_catalog_view, name='magazine_catalog'),
    path('categories-<slug:slug>/', show_categories_view, name='category'),
    path('search/', SearchResultView.as_view(), name='search'),
]
