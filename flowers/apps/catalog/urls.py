from django.urls import path

from apps.catalog.views import magazine_catalog, show_categories, SearchResultView

urlpatterns = [
    path('', magazine_catalog, name='magazine_catalog'),
    path('<slug:slug>/', show_categories, name='category'),
    path('search/', SearchResultView.as_view(), name='search'),
]
