from django.urls import path, include

from apps.cart.views import cart_detail, cart_add, cart_remove, MoreInfo, LikedPages

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('orders/', include(('apps.orders.urls', 'apps.orders'), namespace='orders')),
    path('history/', MoreInfo.as_view(), name='history'),
    path('liked/', LikedPages.as_view(), name='liked'),
]
