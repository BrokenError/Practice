from django.urls import path, include

from apps.products.views import about_us, ShowReviewsView, ShowCommentsView, grade_product_view, AddReviews, \
    AddComments, delete_review, delete_comment, change_comment_view, change_review_view
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
    path('product/<int:product_id>/change-review/<int:review_id>', change_review_view, name='change_review'),
    path('product/<int:product_id>/change-comment/<int:comment_id>', change_comment_view, name='change_comment'),
    path('delete-review/<int:id>', delete_review, name='delete_review'),
    path('delete-comment/<int:id>', delete_comment, name='delete_comment'),
    path('give-grade', grade_product_view, name='give_grade'),
    path('cart/', include('apps.cart.urls')),
]
