from django.urls import path

from apps.user.views import ChangePassword, RegisterUser, logout_user, delete_account, \
    user_personal, user_security, verify_code, user_like, ReplyCommentsView, delete_reply_comment, reply_message_change

urlpatterns = [
    path('', ChangePassword.as_view(), name='user'),
    path('<int:pk_comment>/reply-review/<int:pk_product>', ReplyCommentsView.as_view(), name='add_comments'),
    path('delete-reply-comment/<int:id>', delete_reply_comment, name='delete-reply-comment'),
    path('product/<int:product_id>/comment/<int:comment_id>/<int:replcomment>', reply_message_change,
         name='change-reply-comment'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('delete/', delete_account, name='delete-account'),
    path('security/', user_security, name='security'),
    path('personal/', user_personal, name='personal'),
    path('verify/', verify_code, name='verify'),
    path('like/', user_like, name='like'),
]
