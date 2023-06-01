from django.urls import path, include

from apps.products.views import about_us, ShowReviewsView, ShowCommentsView, grade_product, AddReviews, AddComments
from apps.user.views import LoginUser

urlpatterns = [
    path('', LoginUser.as_view(), name='magazine_home'),
    path('aboutus/', about_us, name='about'),
    path('catalog/', include('apps.catalog.urls')),
    path('user/', include('apps.user.urls')),
    path('reviews/<slug:prod_slug>/', ShowReviewsView.as_view(), name='product'),
    path('comments/<slug:prod_slug>/', ShowCommentsView.as_view(), name='product_comments'),
    path('add-review/<int:pk>', AddReviews.as_view(), name='review'),
    path('add-comment/<int:pk>', AddComments.as_view(), name='comment'),
    path('give-grade', grade_product, name='give_grade'),
    path('cart/', include('apps.cart.urls')),
]
