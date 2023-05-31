from django.urls import path, include

from apps.products.views import about_us, ShowProduct, grade_product, AddReviews
from apps.user.views import LoginUser

urlpatterns = [
    path('', LoginUser.as_view(), name='magazine_home'),
    path('aboutus/', about_us, name='about'),
    path('catalog/', include('apps.catalog.urls')),
    path('user/', include('apps.user.urls')),
    path('<slug:prod_slug>/', ShowProduct.as_view(), name='product'),
    path('review/<int:pk>', AddReviews.as_view(), name='review'),
    path('give-grade', grade_product, name='give_grade'),
    path('cart/', include('apps.cart.urls')),
]
