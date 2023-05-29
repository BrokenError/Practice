from django.urls import path, include
from apps.user.views import LoginUser
from apps.products.views import about_us, show_product, grade_product

urlpatterns = [
    path('', LoginUser.as_view(), name='magazine_home'),
    path('aboutus/', about_us, name='about'),
    path('catalog/', include('apps.catalog.urls')),
    path('user/', include('apps.user.urls')),
    path('<slug:prod_slug>/', show_product, name='product'),
    path('give-grade', grade_product, name='give_grade'),
    path('cart/', include('apps.cart.urls')),
]
